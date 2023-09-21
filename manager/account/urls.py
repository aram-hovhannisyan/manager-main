from django.urls import path
from . import views
from tables.views import (
    save_table_data,
    Paymant_View,
    # Return,
    sendOrder
    )



urlpatterns = [
    path('', views.login_view, name='login_view'),
    path('login/', views.login_view, name='login_view'),
    # path('register/', views.register, name='register'),

    path('adminpage/', views.admin, name='adminpage'),
    
    path('customer/', views.customer, name='customer'),
    path('ohan/', views.ohan, name='ohan'),
    path('kamo/', views.kamo, name="kamo"),

    path('ohan/saveohanstable/', views.ohanSave, name="ohanSave"), 
    path('kamo/savekamostable/', views.kamoSave, name="kamoSave"),


    path('ohan/tables/', views.ohanTables, name="ohanTables"),
    path('kamo/tables/', views.kamoTables, name="kamoTables"),

    path('customers/ohanstbles/', views.tables_by_ohan, name='tablesbyohan'),
    path('customers/kamostbles/', views.tables_by_kamo, name='tablesbykamo'),

    path('employee/', views.employee, name='employee'),
    path('logout/', views.logout_view, name='logout'),
    path('customer/save-table-data/', save_table_data, name='saveTableData'),
    path('delete_item/<int:item_id>/', views.delete_item, name='delete_item'),
    path('delete_item_all/<int:item_id>/', views.delete_item_all, name='delete_item_all'), 
    path('delete_item_byuser/<int:item_id>/', views.delete_item_byuser, name='delete_item_byuser'), 
    path('changeitemsname/', views.cahngeItemsName, name="changeItemsName"),
    




    path('edit_item/<int:item_id>/', views.edit_item, name='edit_item'),
    path('customers/', views.allCustomers, name="customers"),
    path('customers/<int:user_id>/', views.customerTables, name='customertables'),
    path('tablesbycustomer/', views.tablesByUser, name= 'tablesbyuser'),
  
    path('mistake/<int:table_id>/', views.mistakes, name='mistake'),
    path('changes/', views.change, name="changes"),
    path('deletechanges/<int:item_id>/', views.delChange, name="deleteChange"),
    path('endorse/<int:user_id>/', views.endorse, name='endorse'),
    path('endorsechanges/<int:item_id>/', views.endorseChange, name='endorseChange'),


    path('otherItems/', views.otherItems, name='otherItems'),
    path('mainItems/', views.mainItems, name='mainItems'),


    path('customersforAdmin/', views.allCustomersforAdmin, name='customersforadmin'),
    
    path('customerproducts/<int:user_id>/', views.customersProducts, name = 'customersproducts'),
    path('productsforall/', views.productsForAll, name = 'productsforall'),
    
    path('paymant/', Paymant_View, name = 'paymant'),
    # path('return/', Return, name = 'return'),


    # path('debt/<int:user_id>/', views.customerDebt, name = 'customersDebt'),

    path('supplier/', views.supplier, name="supplier"),
    path('supplier/orderedProducts/', views.orderedProducts, name="orderedProducts"),


    # path('toggle-seen/<int:debt_id>/', views.toggle_seen, name='toggle_seen'),
    path('employee/sendorder/', sendOrder, name="sendOrderE"),
    path('mainItems/sendorder/', sendOrder, name="sendOrderM"),
    path('otherItems/sendorder/', sendOrder, name="sendOrderO"),

    path('myorders/<int:supplier_id>/', views.myOrders, name="myorders"),
    # path('sendsalary/', views.sendSalary, name='sendSalary'),
    # path('salaries/', views.salaries, name='salaries')
    path('totalPage/', views.totalPage, name='totalPage')
]
