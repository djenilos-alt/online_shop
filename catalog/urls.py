from django.urls import path

from catalog.views import (
    ContactsView,
    HomeView,
    ProductCreateView,
    ProductDeleteView,
    ProductDetailView,
    ProductUnpublishView,
    ProductUpdateView,
)


urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("contacts/", ContactsView.as_view(), name="contacts"),

    path(
        "products/<int:pk>/",
        ProductDetailView.as_view(),
        name="product_detail",
    ),
    path(
        "products/create/",
        ProductCreateView.as_view(),
        name="product_create",
    ),
    path(
        "products/<int:pk>/update/",
        ProductUpdateView.as_view(),
        name="product_update",
    ),
    path(
        "products/<int:pk>/delete/",
        ProductDeleteView.as_view(),
        name="product_delete",
    ),
    path(
        "products/<int:pk>/unpublish/",
        ProductUnpublishView.as_view(),
        name="product_unpublish",
    ),
]
