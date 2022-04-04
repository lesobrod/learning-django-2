from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import TemplateView, ListView, CreateView, \
    UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from .models import Product, Cart, CartItem, Profile
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from .forms import RegisterForm, ProfileEditForm
from django.forms.models import model_to_dict
from django.contrib import messages


# Product views
class ProductListView(ListView):
    model = Product
    # Пагинация встроена в ListView
    paginate_by = 10
    template_name = "app_goods/product_list.html"
    context_object_name = 'page_obj'

    def post(self, request, *args, **kwargs):
        # TODO что-то с пагинацией
        self.object_list = self.get_queryset()
        # Если у юзера нет профиля


        # Корзины только для инфы! Настоящая корзина - это:
        user_items = CartItem.objects.filter(user=self.request.user)

        # Получаем количества всех товаров в корзине CartItemы данного юзера
        items_values = request.POST.getlist('in-cart')

        flag = False
        for id, value in enumerate(items_values):
            if int(value) > 0:
                # Обрабатываем если есть заказ
                # Находим данный продукт
                this_item = Product.objects.get(id=id + 1)
                flag = True
                if this_item in user_items:
                    # Если продукт уже есть в корзине
                    this_user_item = user_items.get(product=this_item)
                    this_user_item.update(quantity=value + this_user_item.quantity)
                else:
                    # Если его надо добавить
                    CartItem.objects.create(product=this_item,
                                            quantity=value,
                                            cart=Cart.objects.get(user=self.request.user),
                                            user=self.request.user)
        if flag:
            return redirect('list-cartitem')
        else:
            # Если заказов нет, остаемся на странице
            return render(request, self.template_name, self.get_context_data(**kwargs))


class ListCart(ListView):
    model = Cart
    context_object_name = 'carts'
    template_name = 'app_goods/list_carts.html'


class TopListView(ListView):
    model = Product
    context_object_name = 'top_items'
    template_name = 'app_goods/top_items.html'

    def get_queryset(self, **kwargs):
        qs = super().get_queryset()
        return qs.order_by('rate')[:3]


class ListCartItem(ListView):
    model = CartItem
    context_object_name = 'cartitems'
    template_name = 'app_goods/list_cartitems.html'

    def get_queryset(self, **kwargs):
        # Это и есть корзина юзера
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        this_queryset = self.get_queryset()
        items_values = request.POST.getlist('in-cart')
        # Страница видно, только если профиль есть
        profile = Profile.objects.get(user=self.request.user)

        def clear_cart():
            # Очистка корзины
            for item in CartItem.objects.all():
                if item in this_queryset:
                    item.delete()

        if "buy" in request.POST:
            # Списываем стоимость и очищаем
            total_price = 0
            for item, q in zip(this_queryset, items_values):
                total_price += int(item.product.price) * int(q)
            if total_price >= int(profile.balance):
                messages.error(request, 'Баланс недостаточен, пополните!')
                return render(request, self.template_name, self.get_context_data(**kwargs))
            else:
                messages.success(request, 'Покупка совершена!')
                # Рейтинг товара
                for item in this_queryset:
                    item.rate += 1
                    item.save(update_fields=['rate'])
                clear_cart()
                profile.balance = str(int(profile.balance) - total_price)
                # Статус юзера
                profile.status += int(total_price / 100)
                profile.save(update_fields=['balance', 'status'])
                return redirect('main')

        elif "reset" in request.POST:
            # Просто очищаем
            clear_cart()
            return redirect('main')

        elif "save" in request.POST:
            # Просто сохраняем
            return redirect('main')
        else:
            return render(request, self.template_name, self.get_context_data(**kwargs))


class IndexView(TemplateView):
    template_name = 'app_goods/index.html'


class AppLoginView(LoginView):
    template_name = 'app_goods/login.html'


class AppLogoutView(LogoutView):
    template_name = 'app_goods/logout.html'


class AppRegisterView(CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy('main')
    template_name = 'app_goods/register.html'


class AppProfileView(UpdateView):
    model = Profile
    fields = '__all__'
    template_name = 'app_goods/profile.html'


class AppTopBalance(TemplateView):
    template_name = 'app_goods/top_balance.html'

    def post(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=self.request.user)
        profile.balance = str(int(request.POST.get("add")) + int(profile.balance))
        profile.save(update_fields=['balance'])
        return redirect('main')

    def get_context_data(self, **kwargs):
        context = super(AppTopBalance, self).get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(user=self.request.user)
        return context
