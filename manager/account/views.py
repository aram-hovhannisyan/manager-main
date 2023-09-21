from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignUpForm, LoginForm, ItemAddForm
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.db.models import Q

from django.db.models import Case, When, Value, IntegerField


# Create your views here.
from django.contrib.auth.decorators import login_required
from tables.models import (
    ItemsModel,
    UserTable,
    TableItem,
    BigTable,
    Debt,
    Ordered_Products_Column,
    Ordered_Products_Table,
    # Salary,
    JoinedTables,
    Paymant,
    Week_debt,
    Global_Debt,
    Old_debt,
    BigTableRows,
    SingleTable,
    WaitingForChange
)
from account.models import (
    User
)
from datetime import datetime
import json

from django.core.paginator import Paginator

import datetime as d
import random 
from datetime import datetime, timedelta



from django.http import HttpResponseRedirect
from django.db import models
from django.db.models import Sum
from account.mydecorators import (
    admin_required,
    customer_required,
    employee_required,
    supplier_required
)

from .forms import SalaryForm, ChangeItemsName

def index(request):
    return render(request, 'index.html')


def register(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            msg = 'user created'
            return redirect('login_view')
        else:
            msg = 'form is not valid'
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form, 'msg': msg})


def login_view(request):
    form = LoginForm(request.POST or None)
    users = User.objects.all()
    for i in users:
        print(i)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_admin:
                login(request, user)
                return redirect('adminpage')
            elif user is not None and user.is_customer:
                login(request, user)
                if user.username == "Օհան":
                    return redirect('ohan')
                elif user.username == "Կամո":
                    return redirect('kamo')
                else:
                    return redirect('customer')
            elif user is not None and user.is_employee:
                login(request, user)
                return redirect('employee')
            elif user is not None and user.is_supplier:
                login(request, user)
                return redirect('supplier')
        else:
            return redirect('login_view')
    return render(request, 'login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login_view')

# ========================== Customer Start ===================


def create_global_debt(date, user, total):
    try:
        latest_global_debt = Global_Debt.objects.filter(customer=user).latest('timeOfCreating')
        newGlobalDebt = Global_Debt.objects.create(
            customer = user,
            date = date,
            debt = latest_global_debt.debt + total,

        )
    except:
        newGlobalDebt = Global_Debt.objects.create(
            customer = user,
            date = date,
            debt = total
        )

def Create_old_debt(date, user):
    dateObject = datetime.strptime(date, "%Y-%m-%d").date() 
    newUntil = dateObject + timedelta(days=5) 
    try:
        Old_debt.objects.get(
            date = date,
            customer = user
        )
        return
    except:
        try:
            latest_global = Global_Debt.objects.filter(customer=user).latest('timeOfCreating')
            try:
                latest_old_debt = Old_debt.objects.filter(customer=user).latest('timeOfCreating')
                if latest_old_debt.until <= dateObject:
                    Old_debt.objects.create(
                        customer = user,
                        date = date,
                        debt = latest_global.debt,
                        until = newUntil
                    )
                    # print('created', latest_old_debt.until <= dateObject)
            except:
                Old_debt.objects.create(
                    customer = user,
                    date = date,
                    debt = latest_global.debt,
                    until = newUntil
                )
        except:
            Old_debt.objects.create(
                customer = user,
                date = date,
                debt = 0,
                until = newUntil
            )


# OHAN OHAN OHAN 

def ohanSave(request):
    if request.method == 'POST':
        try:
            # sups = ['Արտադրամաս',"Փուռ","Կիրովական"]
            art = User.objects.get(username="Արտադրամաս")
            pur = User.objects.get(username="Փուռ")
            kir = User.objects.get(username="Կիրովական")
            data = json.loads(request.body.decode('utf-8'))
            date = data.get('date')
            ohanUser = User.objects.get(username = 'Օհան')
            gavarUser = User.objects.get(username = 'Գ.4-րդ')
            avagUser = User.objects.get(username = 'Գ.ավագ')
            araUser = User.objects.get(username = 'Արա')

            totalSums = data.get('totalSums', {})
            # print(totalSums)
 
            ohanJoin = JoinedTables.objects.create(
                    tableName='ohan' + str(random.uniform(1.0, 100.0))[:15],
                    customer=ohanUser,
                    dateOfCreating=date
            )
            gavarJoin = JoinedTables.objects.create(
                    tableName='gavar' + str(random.uniform(1.0, 100.0))[:15],
                    customer=gavarUser,
                    dateOfCreating=date
            )
            avagJoin = JoinedTables.objects.create(
                    tableName='avag' + str(random.uniform(1.0, 100.0))[:15],
                    customer=avagUser,
                    dateOfCreating=date
            )
            araJoin = JoinedTables.objects.create(
                    tableName='ara' + str(random.uniform(1.0, 100.0))[:15],
                    customer=araUser,
                    dateOfCreating=date
            )
            # ohan start
            ohanArt = UserTable.objects.create(
                    user=ohanUser,
                    tableName='ohanArt' + str(random.uniform(1.0, 100.0))[:15],
                    dateOfCreating=date,
                    joinedTable=ohanJoin,
                )           
            ohanPur = UserTable.objects.create(
                    user=ohanUser,
                    tableName='ohanPur' + str(random.uniform(1.0, 100.0))[:15],
                    dateOfCreating=date,
                    joinedTable=ohanJoin,
                )
            ohanKir = UserTable.objects.create(
                    user=ohanUser,
                    tableName='ohanKir' + str(random.uniform(1.0, 100.0))[:15],
                    dateOfCreating=date,
                    joinedTable=ohanJoin,
                )
            # ohan end
            gavarArt = UserTable.objects.create(
                    user=gavarUser,
                    tableName='gavarArt' + str(random.uniform(1.0, 100.0))[:15],
                    dateOfCreating=date,
                    joinedTable=gavarJoin,
                )
            gavarPur = UserTable.objects.create(
                    user=gavarUser,
                    tableName='gavarPur' + str(random.uniform(1.0, 100.0))[:15],
                    dateOfCreating=date,
                    joinedTable=gavarJoin,
                )
            gavarKir = UserTable.objects.create(
                    user=gavarUser,
                    tableName='gavarKir' + str(random.uniform(1.0, 100.0))[:15],
                    dateOfCreating=date,
                    joinedTable=gavarJoin,
                )
            # gavar end 
            avagArt = UserTable.objects.create(
                    user=avagUser,
                    tableName='avagArt' + str(random.uniform(1.0, 100.0))[:15],
                    dateOfCreating=date,
                    joinedTable=avagJoin,
                )
            avagPur = UserTable.objects.create(
                    user=avagUser,
                    tableName='avagPur' + str(random.uniform(1.0, 100.0))[:15],
                    dateOfCreating=date,
                    joinedTable=avagJoin,
                )
            avagKir = UserTable.objects.create(
                    user=avagUser,
                    tableName='avagKir' + str(random.uniform(1.0, 100.0))[:15],
                    dateOfCreating=date,
                    joinedTable=avagJoin,
                )
            # avag end
            araArt = UserTable.objects.create(
                    user=araUser,
                    tableName='araArt' + str(random.uniform(1.0, 100.0))[:15],
                    dateOfCreating=date,
                    joinedTable=araJoin,
                )
            araPur = UserTable.objects.create(
                    user=araUser,
                    tableName='araPur' + str(random.uniform(1.0, 100.0))[:15],
                    dateOfCreating=date,
                    joinedTable=araJoin,
                )
            araKir = UserTable.objects.create(
                    user=araUser,
                    tableName='araKir' + str(random.uniform(1.0, 100.0))[:15],
                    dateOfCreating=date,
                    joinedTable=araJoin,
                )

            ohan_data = data.get('ohan', [])
            gavar_data = data.get('gavar', [])
            avag_data = data.get('avag', [])
            ara_data = data.get('ara', [])

            for oh in ohan_data:
                if oh['supplier'] == 'Արտադրամաս':
                    table_item = TableItem.objects.create(
                        table = ohanArt,
                        product_name = oh['productName'],
                        product_count = oh['productCount'],
                        product_price = oh['price'],
                        total_price = oh['totalPrice'],
                        customer = ohanUser,
                        supplier = art,
                        supTotal = oh['supTotal']
                    )
                    try:
                        big_tab = BigTableRows.objects.get(
                            user=ohanUser, 
                            supplier=art,
                            porduct_name=oh['productName']
                            )
                        big_tab.item = table_item
                        big_tab.save()
                    except:
                        big_tab = BigTableRows.objects.create(
                            user=ohanUser, 
                            supplier=art, 
                            item=table_item,
                            porduct_name=oh['productName']
                            )
                        big_tab.save()
                elif oh['supplier'] == 'Փուռ':
                    table_item = TableItem.objects.create(
                        table = ohanPur,
                        product_name = oh['productName'],
                        product_count = oh['productCount'],
                        product_price = oh['price'],
                        total_price = oh['totalPrice'],
                        customer = ohanUser,
                        supplier = art,
                        supTotal = oh['supTotal']
                    )
                    try:
                        big_tab = BigTableRows.objects.get(
                            user=ohanUser, 
                            supplier=pur,
                            porduct_name=oh['productName']
                            )
                        big_tab.item = table_item
                        big_tab.save()
                    except:
                        big_tab = BigTableRows.objects.create(
                            user=ohanUser, 
                            supplier=pur, 
                            item=table_item,
                            porduct_name=oh['productName']
                            )
                        big_tab.save()
                elif oh['supplier'] == 'Կիրովական':
                    table_item = TableItem.objects.create(
                        table = ohanKir,
                        product_name = oh['productName'],
                        product_count = oh['productCount'],
                        product_price = oh['price'],
                        total_price = oh['totalPrice'],
                        customer = ohanUser,
                        supplier = art,
                        supTotal = oh['supTotal']
                    )
                    try:
                        big_tab = BigTableRows.objects.get(
                            user=ohanUser, 
                            supplier=kir,
                            porduct_name=oh['productName']
                            )
                        big_tab.item = table_item
                        big_tab.save()
                    except:
                        big_tab = BigTableRows.objects.create(
                            user=ohanUser, 
                            supplier=kir, 
                            item=table_item,
                            porduct_name=oh['productName']
                            )
                        big_tab.save()
            for oh in gavar_data:
                if oh['supplier'] == 'Արտադրամաս':
                    table_item = TableItem.objects.create(
                        table = gavarArt,
                        product_name = oh['productName'],
                        product_count = oh['productCount'],
                        product_price = oh['price'],
                        total_price = oh['totalPrice'],
                        customer = gavarUser,
                        supplier = art,
                        supTotal = oh['supTotal']
                    )
                    try:
                        big_tab = BigTableRows.objects.get(
                            user=gavarUser, 
                            supplier=art,
                            porduct_name=oh['productName']
                            )
                        big_tab.item = table_item
                        big_tab.save()
                    except:
                        big_tab = BigTableRows.objects.create(
                            user=gavarUser, 
                            supplier=art, 
                            item=table_item,
                            porduct_name=oh['productName']
                            )
                        big_tab.save()
                elif oh['supplier'] == 'Փուռ':
                    table_item = TableItem.objects.create(
                        table = gavarPur,
                        product_name = oh['productName'],
                        product_count = oh['productCount'],
                        product_price = oh['price'],
                        total_price = oh['totalPrice'],
                        customer = gavarUser,
                        supplier = pur,
                        supTotal = oh['supTotal']
                    )
                    try:
                        big_tab = BigTableRows.objects.get(
                            user=gavarUser, 
                            supplier=pur,
                            porduct_name=oh['productName']
                            )
                        big_tab.item = table_item
                        big_tab.save()
                    except:
                        big_tab = BigTableRows.objects.create(
                            user=gavarUser, 
                            supplier=pur, 
                            item=table_item,
                            porduct_name=oh['productName']
                            )
                        big_tab.save()
                elif oh['supplier'] == 'Կիրովական':
                    table_item = TableItem.objects.create(
                        table = gavarKir,
                        product_name = oh['productName'],
                        product_count = oh['productCount'],
                        product_price = oh['price'],
                        total_price = oh['totalPrice'],
                        customer = gavarUser,
                        supplier = kir,
                        supTotal = oh['supTotal']
                    )
                    try:
                        big_tab = BigTableRows.objects.get(
                            user=gavarUser, 
                            supplier=kir,
                            porduct_name=oh['productName']
                            )
                        big_tab.item = table_item
                        big_tab.save()
                    except:
                        big_tab = BigTableRows.objects.create(
                            user=gavarUser, 
                            supplier=kir, 
                            item=table_item,
                            porduct_name=oh['productName']
                            )
                        big_tab.save()
            for oh in avag_data:
                if oh['supplier'] == 'Արտադրամաս':
                    table_item = TableItem.objects.create(
                        table = avagArt,
                        product_name = oh['productName'],
                        product_count = oh['productCount'],
                        product_price = oh['price'],
                        total_price = oh['totalPrice'],
                        customer = avagUser,
                        supplier = art,
                        supTotal = oh['supTotal']
                    )
                    try:
                        big_tab = BigTableRows.objects.get(
                            user=avagUser, 
                            supplier=art,
                            porduct_name=oh['productName']
                            )
                        big_tab.item = table_item
                        big_tab.save()
                    except:
                        big_tab = BigTableRows.objects.create(
                            user=avagUser, 
                            supplier=art, 
                            item=table_item,
                            porduct_name=oh['productName']
                            )
                        big_tab.save()
                elif oh['supplier'] == 'Փուռ':
                    table_item = TableItem.objects.create(
                        table = avagPur,
                        product_name = oh['productName'],
                        product_count = oh['productCount'],
                        product_price = oh['price'],
                        total_price = oh['totalPrice'],
                        customer = avagUser,
                        supplier = pur,
                        supTotal = oh['supTotal']
                    )
                    try:
                        big_tab = BigTableRows.objects.get(
                            user=avagUser, 
                            supplier=pur,
                            porduct_name=oh['productName']
                            )
                        big_tab.item = table_item
                        big_tab.save()
                    except:
                        big_tab = BigTableRows.objects.create(
                            user=avagUser, 
                            supplier=pur, 
                            item=table_item,
                            porduct_name=oh['productName']
                            )
                        big_tab.save()
                elif oh['supplier'] == 'Կիրովական':
                    table_item = TableItem.objects.create(
                        table = avagKir,
                        product_name = oh['productName'],
                        product_count = oh['productCount'],
                        product_price = oh['price'],
                        total_price = oh['totalPrice'],
                        customer = avagUser,
                        supplier = kir,
                        supTotal = oh['supTotal']
                    )
                    try:
                        big_tab = BigTableRows.objects.get(
                            user=avagUser, 
                            supplier=kir,
                            porduct_name=oh['productName']
                            )
                        big_tab.item = table_item
                        big_tab.save()
                    except:
                        big_tab = BigTableRows.objects.create(
                            user=avagUser, 
                            supplier=kir, 
                            item=table_item,
                            porduct_name=oh['productName']
                            )
                        big_tab.save()
            for ar in ara_data:
                if ar['supplier'] == 'Արտադրամաս':
                    table_item = TableItem.objects.create(
                        table = araArt,
                        product_name = ar['productName'],
                        product_count = ar['productCount'],
                        product_price = ar['price'],
                        total_price = ar['totalPrice'],
                        customer = araUser,
                        supplier = art,
                        supTotal = ar['supTotal']
                    )
                    try:
                        big_tab = BigTableRows.objects.get(
                            user=araUser, 
                            supplier=art,
                            porduct_name=ar['productName']
                            )
                        big_tab.item = table_item
                        big_tab.save()
                    except:
                        big_tab = BigTableRows.objects.create(
                            user=araUser, 
                            supplier=art, 
                            item=table_item,
                            porduct_name=ar['productName']
                            )
                        big_tab.save()
                elif ar['supplier'] == 'Փուռ':
                    table_item = TableItem.objects.create(
                        table = araPur,
                        product_name = ar['productName'],
                        product_count = ar['productCount'],
                        product_price = ar['price'],
                        total_price = ar['totalPrice'],
                        customer = araUser,
                        supplier = pur,
                        supTotal = ar['supTotal']
                    )
                    try:
                        big_tab = BigTableRows.objects.get(
                            user=araUser, 
                            supplier=pur,
                            porduct_name=ar['productName']
                            )
                        big_tab.item = table_item
                        big_tab.save()
                    except:
                        big_tab = BigTableRows.objects.create(
                            user=araUser, 
                            supplier=pur, 
                            item=table_item,
                            porduct_name=ar['productName']
                            )
                        big_tab.save()
                elif ar['supplier'] == 'Կիրովական':
                    table_item = TableItem.objects.create(
                        table = araKir,
                        product_name = ar['productName'],
                        product_count = ar['productCount'],
                        product_price = ar['price'],
                        total_price = ar['totalPrice'],
                        customer = araUser,
                        supplier = kir,
                        supTotal = ar['supTotal']
                    )
                    try:
                        big_tab = BigTableRows.objects.get(
                            user=araUser, 
                            supplier=kir,
                            porduct_name=ar['productName']
                            )
                        big_tab.item = table_item
                        big_tab.save()
                    except:
                        big_tab = BigTableRows.objects.create(
                            user=araUser, 
                            supplier=kir, 
                            item=table_item,
                            porduct_name=ar['productName']
                            )
                        big_tab.save()
            Debt.objects.create(
                customer = ohanUser,
                joined = True,
                debt = totalSums['ohantotalSum'],
                date = date
            )
            Create_old_debt(date, ohanUser)
            create_global_debt(date, ohanUser, totalSums['ohantotalSum'])
            Debt.objects.create(
                customer = gavarUser,
                joined = True,
                debt = totalSums['gavartotalSum'],
                date = date
            )
            Create_old_debt(date, gavarUser)        
            create_global_debt(date, gavarUser, totalSums['gavartotalSum'])
            Debt.objects.create(
                customer = avagUser,
                joined = True,
                debt = totalSums['avagtotalSum'],
                date = date
            )
            Create_old_debt(date, avagUser)
            create_global_debt(date, avagUser, totalSums['avagtotalSum'])
            Debt.objects.create(
                customer = araUser,
                joined = True,
                debt = totalSums['aratotalSum'],
                date = date
            )
            Create_old_debt(date, araUser)
            create_global_debt(date, araUser, totalSums['aratotalSum'])
            # suppliers = [art, pur, kir]
            custs = [ohanUser,gavarUser,avagUser,araUser]

            ArtTable = [ohanArt,gavarArt,avagArt,araArt]
            purTable = [ohanPur,gavarPur,avagPur,araPur]
            kirTable = [ohanKir,gavarKir,avagKir,araKir]

            for at,cust in zip(ArtTable, custs):
                try:
                    bigtable = BigTable.objects.get(supplier=art, user=cust)
                    bigtable.table = at
                    bigtable.modifiedDate = date
                    bigtable.save()
                except:
                    # print(at, cust)
                    bigtable = BigTable.objects.create(
                        supplier=art,
                        table=at,
                        user=cust,
                        modifiedDate=date
                        )
            for pt,cust in zip(purTable, custs):
                try:
                    bigtable = BigTable.objects.get(supplier=pur, user=cust)
                    bigtable.table = pt
                    bigtable.modifiedDate = date
                    bigtable.save()
                except:
                    bigtable = BigTable.objects.create(
                        supplier=pur,
                        table=pt,
                        user=cust,
                        modifiedDate=date
                        )
            for kt,cust in zip(kirTable, custs):
                try:
                    bigtable = BigTable.objects.get(supplier=kir, user=cust)
                    bigtable.table = kt
                    bigtable.modifiedDate = date
                    bigtable.save()
                except:
                    bigtable = BigTable.objects.create(
                        supplier=kir,
                        table=kt,
                        user=cust,
                        modifiedDate=date
                        )
            
            return JsonResponse({'message': 'Data received and processed successfully'})
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


def kamoSave(request):
    if request.method == 'POST':
            art = User.objects.get(username="Արտադրամաս")
            pur = User.objects.get(username="Փուռ")
            kir = User.objects.get(username="Կիրովական")
            
            data = json.loads(request.body.decode('utf-8'))
            # print(data)
            date = data.get('date')
            kamo_User = User.objects.get(username = 'Կամո')
            gandak_User = User.objects.get(username = 'Գանձակ')
            sarukan_User = User.objects.get(username = 'Սարուխան')

            totalSums = data.get('totalSums', {})

            kamoJoin = JoinedTables.objects.create(
                    tableName='kamo' + str(random.uniform(1.0, 100.0))[:15],
                    customer=kamo_User,
                    dateOfCreating=date
            )
            gandakJoin = JoinedTables.objects.create(
                    tableName='gandak' + str(random.uniform(1.0, 100.0))[:15],
                    customer=gandak_User,
                    dateOfCreating=date
            )
            sarukanJoin = JoinedTables.objects.create(
                    tableName='sarukan' + str(random.uniform(1.0, 100.0))[:15],
                    customer=sarukan_User,
                    dateOfCreating=date
            )

            kamoArt = UserTable.objects.create(
                    user=kamo_User,
                    tableName='kamoArt' + str(random.uniform(1.0, 100.0))[:15],
                    dateOfCreating=date,
                    joinedTable=kamoJoin,
                )           
            kamoPur = UserTable.objects.create(
                    user=kamo_User,
                    tableName='kamoPur' + str(random.uniform(1.0, 100.0))[:15],
                    dateOfCreating=date,
                    joinedTable=kamoJoin,
                )
            kamoKir = UserTable.objects.create(
                    user=kamo_User,
                    tableName='kamoKir' + str(random.uniform(1.0, 100.0))[:15],
                    dateOfCreating=date,
                    joinedTable=kamoJoin,
                )
            # ohan end

            gandakArt = UserTable.objects.create(
                    user=gandak_User,
                    tableName='gandakArt' + str(random.uniform(1.0, 100.0))[:15],
                    dateOfCreating=date,
                    joinedTable=gandakJoin,
                )
            gandakPur = UserTable.objects.create(
                    user=gandak_User,
                    tableName='gandakPur' + str(random.uniform(1.0, 100.0))[:15],
                    dateOfCreating=date,
                    joinedTable=gandakJoin,
                )
            gandakKir = UserTable.objects.create(
                    user=gandak_User,
                    tableName='gandakKir' + str(random.uniform(1.0, 100.0))[:15],
                    dateOfCreating=date,
                    joinedTable=gandakJoin,
                )
            # gavar end 

            sarukanArt = UserTable.objects.create(
                    user=sarukan_User,
                    tableName='sarukanArt' + str(random.uniform(1.0, 100.0))[:15],
                    dateOfCreating=date,
                    joinedTable=sarukanJoin,
                )
            sarukanPur = UserTable.objects.create(
                    user=sarukan_User,
                    tableName='sarukanPur' + str(random.uniform(1.0, 100.0))[:15],
                    dateOfCreating=date,
                    joinedTable=sarukanJoin,
                )
            sarukanKir = UserTable.objects.create(
                    user=sarukan_User,
                    tableName='sarukanKir' + str(random.uniform(1.0, 100.0))[:15],
                    dateOfCreating=date,
                    joinedTable=sarukanJoin,
                )
          
            kamo_data = data.get('kamo', [])
            gandak_data = data.get('gandak', [])
            sarukan_data = data.get('sarukan', [])

            for oh in kamo_data:
                if oh['supplier'] == 'Արտադրամաս':
                    table_item = TableItem.objects.create(
                        table = kamoArt,
                        product_name = oh['productName'],
                        product_count = oh['productCount'],
                        product_price = oh['price'],
                        total_price = oh['totalPrice'],
                        customer = kamo_User,
                        supplier = art,
                        supTotal = oh['supTotal']
                    )
                    try:
                        big_tab = BigTableRows.objects.get(
                            user=kamo_User, 
                            supplier=art,
                            porduct_name=oh['productName']
                            )
                        big_tab.item = table_item
                        big_tab.save()
                    except:
                        big_tab = BigTableRows.objects.create(
                            user=kamo_User, 
                            supplier=art, 
                            item=table_item,
                            porduct_name=oh['productName']
                            )
                        big_tab.save()
                elif oh['supplier'] == 'Փուռ':
                    table_item = TableItem.objects.create(
                        table = kamoPur,
                        product_name = oh['productName'],
                        product_count = oh['productCount'],
                        product_price = oh['price'],
                        total_price = oh['totalPrice'],
                        customer = kamo_User,
                        supplier = art,
                        supTotal = oh['supTotal']
                    )
                    try:
                        big_tab = BigTableRows.objects.get(
                            user=kamo_User, 
                            supplier=pur,
                            porduct_name=oh['productName']
                            )
                        big_tab.item = table_item
                        big_tab.save()
                    except:
                        big_tab = BigTableRows.objects.create(
                            user=kamo_User, 
                            supplier=pur, 
                            item=table_item,
                            porduct_name=oh['productName']
                            )
                        big_tab.save()
                elif oh['supplier'] == 'Կիրովական':
                    table_item = TableItem.objects.create(
                        table = kamoKir,
                        product_name = oh['productName'],
                        product_count = oh['productCount'],
                        product_price = oh['price'],
                        total_price = oh['totalPrice'],
                        customer = kamo_User,
                        supplier = art,
                        supTotal = oh['supTotal']
                    )
                    try:
                        big_tab = BigTableRows.objects.get(
                            user=kamo_User, 
                            supplier=kir,
                            porduct_name=oh['productName']
                            )
                        big_tab.item = table_item
                        big_tab.save()
                    except:
                        big_tab = BigTableRows.objects.create(
                            user=kamo_User, 
                            supplier=kir, 
                            item=table_item,
                            porduct_name=oh['productName']
                            )
                        big_tab.save()

            for oh in gandak_data:
                if oh['supplier'] == 'Արտադրամաս':
                    table_item = TableItem.objects.create(
                        table = gandakArt,
                        product_name = oh['productName'],
                        product_count = oh['productCount'],
                        product_price = oh['price'],
                        total_price = oh['totalPrice'],
                        customer = gandak_User,
                        supplier = art,
                        supTotal = oh['supTotal']
                    )
                    try:
                        big_tab = BigTableRows.objects.get(
                            user=gandak_User, 
                            supplier=art,
                            porduct_name=oh['productName']
                            )
                        big_tab.item = table_item
                        big_tab.save()
                    except:
                        big_tab = BigTableRows.objects.create(
                            user=gandak_User, 
                            supplier=art, 
                            item=table_item,
                            porduct_name=oh['productName']
                            )
                        big_tab.save()
                elif oh['supplier'] == 'Փուռ':
                    table_item = TableItem.objects.create(
                        table = gandakPur,
                        product_name = oh['productName'],
                        product_count = oh['productCount'],
                        product_price = oh['price'],
                        total_price = oh['totalPrice'],
                        customer = gandak_User,
                        supplier = pur,
                        supTotal = oh['supTotal']
                    )
                    try:
                        big_tab = BigTableRows.objects.get(
                            user=gandak_User, 
                            supplier=pur,
                            porduct_name=oh['productName']
                            )
                        big_tab.item = table_item
                        big_tab.save()
                    except:
                        big_tab = BigTableRows.objects.create(
                            user=gandak_User, 
                            supplier=pur, 
                            item=table_item,
                            porduct_name=oh['productName']
                            )
                        big_tab.save()
                elif oh['supplier'] == 'Կիրովական':
                    table_item = TableItem.objects.create(
                        table = gandakKir,
                        product_name = oh['productName'],
                        product_count = oh['productCount'],
                        product_price = oh['price'],
                        total_price = oh['totalPrice'],
                        customer = gandak_User,
                        supplier = kir,
                        supTotal = oh['supTotal']
                    )
                    try:
                        big_tab = BigTableRows.objects.get(
                            user=gandak_User, 
                            supplier=kir,
                            porduct_name=oh['productName']
                            )
                        big_tab.item = table_item
                        big_tab.save()
                    except:
                        big_tab = BigTableRows.objects.create(
                            user=gandak_User, 
                            supplier=kir, 
                            item=table_item,
                            porduct_name=oh['productName']
                            )
                        big_tab.save()

            for oh in sarukan_data:
                if oh['supplier'] == 'Արտադրամաս':
                    table_item = TableItem.objects.create(
                        table = sarukanArt,
                        product_name = oh['productName'],
                        product_count = oh['productCount'],
                        product_price = oh['price'],
                        total_price = oh['totalPrice'],
                        customer = sarukan_User,
                        supplier = art,
                        supTotal = oh['supTotal']
                    )
                    try:
                        big_tab = BigTableRows.objects.get(
                            user=sarukan_User, 
                            supplier=art,
                            porduct_name=oh['productName']
                            )
                        big_tab.item = table_item
                        big_tab.save()
                    except:
                        big_tab = BigTableRows.objects.create(
                            user=sarukan_User, 
                            supplier=art, 
                            item=table_item,
                            porduct_name=oh['productName']
                            )
                        big_tab.save()
                elif oh['supplier'] == 'Փուռ':
                    table_item = TableItem.objects.create(
                        table = sarukanPur,
                        product_name = oh['productName'],
                        product_count = oh['productCount'],
                        product_price = oh['price'],
                        total_price = oh['totalPrice'],
                        customer = sarukan_User,
                        supplier = pur,
                        supTotal = oh['supTotal']
                    )
                    try:
                        big_tab = BigTableRows.objects.get(
                            user=sarukan_User, 
                            supplier=pur,
                            porduct_name=oh['productName']
                            )
                        big_tab.item = table_item
                        big_tab.save()
                    except:
                        big_tab = BigTableRows.objects.create(
                            user=sarukan_User, 
                            supplier=pur, 
                            item=table_item,
                            porduct_name=oh['productName']
                            )
                        big_tab.save()
                elif oh['supplier'] == 'Կիրովական':
                    table_item = TableItem.objects.create(
                        table = sarukanKir,
                        product_name = oh['productName'],
                        product_count = oh['productCount'],
                        product_price = oh['price'],
                        total_price = oh['totalPrice'],
                        customer = sarukan_User,
                        supplier = kir,
                        supTotal = oh['supTotal']
                    )
                    try:
                        big_tab = BigTableRows.objects.get(
                            user=sarukan_User, 
                            supplier=kir,
                            porduct_name=oh['productName']
                            )
                        big_tab.item = table_item
                        big_tab.save()
                    except:
                        big_tab = BigTableRows.objects.create(
                            user=sarukan_User, 
                            supplier=kir, 
                            item=table_item,
                            porduct_name=oh['productName']
                            )
                        big_tab.save()
  
            Debt.objects.create(
                customer = kamo_User,
                joined = True,
                debt = totalSums['kamototalSum'],
                date = date
            )
            Create_old_debt(date, kamo_User)
            create_global_debt(date, kamo_User, totalSums['kamototalSum'])

            Debt.objects.create(
                customer = gandak_User,
                joined = True,
                debt = totalSums['gandaktotalSum'],
                date = date
            )
            Create_old_debt(date, gandak_User)  
            create_global_debt(date, gandak_User, totalSums['gandaktotalSum'])

            Debt.objects.create(
                customer = sarukan_User,
                joined = True,
                debt = totalSums['sarukamtotalSum'],
                date = date
            )
            Create_old_debt(date, sarukan_User)
            create_global_debt(date, sarukan_User, totalSums['sarukamtotalSum'])

            custs = [kamo_User,gandak_User,sarukan_User]

            ArtTable = [kamoArt,gandakArt,sarukanArt]
            purTable = [kamoPur,gandakPur,sarukanPur]
            kirTable = [kamoKir,gandakKir,sarukanKir]

            for at,cust in zip(ArtTable, custs):
                try:
                    bigtable = BigTable.objects.get(supplier=art, user=cust)
                    bigtable.table = at
                    bigtable.modifiedDate = date
                    bigtable.save()
                except:
                    # print(at, cust)
                    bigtable = BigTable.objects.create(
                        supplier=art,
                        table=at,
                        user=cust,
                        modifiedDate=date
                        )
            for pt,cust in zip(purTable, custs):
                try:
                    bigtable = BigTable.objects.get(supplier=pur, user=cust)
                    bigtable.table = pt
                    bigtable.modifiedDate = date
                    bigtable.save()
                except:
                    bigtable = BigTable.objects.create(
                        supplier=pur,
                        table=pt,
                        user=cust,
                        modifiedDate=date
                        )
            for kt,cust in zip(kirTable, custs):
                try:
                    bigtable = BigTable.objects.get(supplier=kir, user=cust)
                    bigtable.table = kt
                    bigtable.modifiedDate = date
                    bigtable.save()
                except:
                    bigtable = BigTable.objects.create(
                        supplier=kir,
                        table=kt,
                        user=cust,
                        modifiedDate=date
                        )
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            # return redirect(request.path_info)
            # return JsonResponse({'message': 'Data received and processed successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

def kamo(request):
    usersArray = [
        'Կամո',
        'Գանձակ',
        'Սարուխան'
    ]
    for i, v in enumerate(usersArray):
        usersArray[i] = User.objects.get(username = v)

    itemsObjects = {
        'kamo':[],
        'gandak':[],
        'sarukan':[]
    }

    for user, us in zip(usersArray, itemsObjects):
        itemsObjects[us] = ItemsModel.objects.filter(customer=user.username)
    
    Items = []
    uniq = ItemsModel.productsfor_Customer(request.user)

    for prod,kamo,gandak,sarukan in zip(uniq,itemsObjects['kamo'], itemsObjects['gandak'], itemsObjects['sarukan']):
        Items.append(
            [prod.productName,kamo,gandak,sarukan]
        )
    return render(request, 'drivers/kamo.html',   {
        'Items': Items
    })

def kamoTables(request):
    page_number = request.GET.get('page')
    # Joined Tables
    kamo_User = request.user
    joinedTables = JoinedTables.objects.filter(
        customer=kamo_User,
        ).order_by('timeOfCreating')  # Reverse the order by '-id'
    joinPaginator = Paginator(joinedTables, 5)  # show 5 joinedTables per page
    join_page_obj = joinPaginator.get_page(page_number)
    reversed_join_page_obj = joinPaginator.get_page(
            joinPaginator.num_pages - join_page_obj.number + 1
        ).__reversed__()  # Reversed join_page_obj
    customers = [
        User.objects.get(username='Կամո'),
        User.objects.get(username='Գանձակ'),
        User.objects.get(username='Սարուխան')
        ]

    tables = []

    joinedTables_array = []
    for ohan_join in reversed_join_page_obj:
        mini_arr = []
        tables.append(ohan_join)
        for join in JoinedTables.objects.filter(dateOfCreating = ohan_join.dateOfCreating, customer__in = customers):
            mini_arr.append(join)
        joinedTables_array.append(mini_arr)
    
    joined_Max = []
    for i in joinedTables_array:
        for j in i:
            joined_Max.append(j)

    userTables = UserTable.objects.filter(joinedTable__in = joined_Max)
    userTables_array = []
    for us in userTables:
        userTables_array.append(us)

    suppliers = ['Արտադրամաս','Փուռ','Կիրովական']
    uniq = ItemsModel.productsfor_Customer(kamo_User)
    rows = []
    for joined_arr in joinedTables_array:
        mini_rows = []
        # print(joined_arr)
        for joinedTable in joined_arr:
            table_Rows = []
            for userTable in userTables_array:
                if userTable.joinedTable == joinedTable:
                    for product in uniq:
                        if product.supplier in suppliers:
                            try:
                                if joinedTable.customer.username == 'Կամո':
                                    us = 'kamo'
                                elif joinedTable.customer.username == 'Գանձակ':
                                    us = 'gandak'
                                elif joinedTable.customer.username == 'Սարուխան':
                                    us = "sarukan"
                                r = {
                                    'productName': product.productName, 
                                    us: TableItem.objects.get(
                                        table=userTable,
                                        product_name=product.productName,
                                        customer=joinedTable.customer
                                )}
                                table_Rows.append(r)
                            except:
                                pass
            if joinedTable.customer.username == 'Կամո':
                ts = 'kamo'
            elif joinedTable.customer.username == 'Գանձակ':
                ts = 'gandak'
            elif joinedTable.customer.username == 'Սարուխան':
                ts = "sarukan"             
            mini_rows.append({
                'table_name': f'{joinedTable.tableName}',
                ts : table_Rows
                })
        rows.append(mini_rows)

    complete_row = []

    for tab in tables:
        mini_comp = []
        kamo_total = 0
        gandak_total = 0
        sarukan_total = 0
        big_total = 0
        for row in rows:
            # print(row[3]['ohan'])

            if row[2]['table_name'] == tab.tableName:
                for prod in uniq:
                    row_list = []
                    total_of_row = 0
                    row_list.append(prod.productName)
                        # print(ohan)
                    for kamo in row[2]['kamo']:
                        if kamo['productName'] == prod.productName:
                            row_list.append(kamo['kamo'])
                            total_of_row += kamo['kamo'].total_price
                            kamo_total += kamo['kamo'].total_price
                            break
                    for gandak in row[1]['gandak']:
                        if gandak['productName'] == prod.productName:
                            row_list.append(gandak['gandak'])
                            total_of_row += gandak['gandak'].total_price
                            gandak_total += gandak['gandak'].total_price
                            break
                    for sarukan in row[0]['sarukan']:
                        if sarukan['productName'] == prod.productName:
                            row_list.append(sarukan['sarukan'])
                            total_of_row += sarukan['sarukan'].total_price
                            sarukan_total += sarukan['sarukan'].total_price
                            break
                    row_list.append(total_of_row)
                    big_total += total_of_row
                    mini_comp.append(row_list)

                # print(mini_comp)
        complete_row.append({f'{tab.tableName}':mini_comp,'last_row': ['Ընդ', kamo_total, gandak_total, sarukan_total, big_total]})        

    joineddebt = Debt.objects.filter(
        customer = User.objects.get(username = "Կամո"),
        joined = True
        ).order_by('timeOfCreating')
    joineddebtPaginator = Paginator(joineddebt, 5) #show 5 debts per page of the joined tables
    joineddebt_page_obj = joineddebtPaginator.get_page(page_number)
    reversed_joined_debt_obj = joineddebtPaginator.get_page(
        joineddebtPaginator.num_pages - joineddebt_page_obj.number + 1
    )
    single_debt_array = []
    single_debt_dict = {}
    for i in reversed_joined_debt_obj:
        try: 
            singleDebt = Debt.objects.filter(
                single=True, 
                date=i.date,
                customer__in=customers
                )
            if singleDebt[0].date not in single_debt_array:
                single_debt_array.append(singleDebt[0].date)
                single_debt_dict[str(i.date)] = singleDebt.aggregate(sum = Sum('debt'))['sum']
        except:
            continue
    debt_array = []
    for debt in reversed_joined_debt_obj:
        joinTable_debt = Debt.objects.filter(
            joined = True,
            date = debt.date,
            customer__in=customers
        )
        try:
            debt_array.append([str(debt.date),joinTable_debt.aggregate(sum = Sum('debt'))['sum'], single_debt_dict[str(debt.date)]])
        except:
            debt_array.append([str(debt.date),joinTable_debt.aggregate(sum = Sum('debt'))['sum'], ''])
    # PAYMANT
    try:
        total_payments_money = Paymant.objects.filter(
            date = single_debt_array[0],
        ).aggregate(money=models.Sum('money'))['money']
        total_payments_returned = Paymant.objects.filter(
            date = single_debt_array[0],
        ).aggregate(returned=models.Sum('returned'))['returned']
        total_payments_salary = Paymant.objects.filter(
            date = single_debt_array[0],
        ).aggregate(salary=models.Sum('salary'))['salary']
    except:
        total_payments_money = 0
        total_payments_returned = 0
        total_payments_salary = 0

    total_global_debt = 0
    try:
        old_debt = Old_debt.objects.filter(date = single_debt_array[0], customer__in=customers).aggregate(sum = Sum('debt'))['sum']
        new_debt = Week_debt.objects.filter(date = single_debt_array[0], customer__in=customers).aggregate(sum = Sum('debt'))['sum']
    except:
        old_debt = 0
        new_debt = 0
        pass
    for customer in customers:
        debt = Global_Debt.objects.filter(customer=customer).order_by('-timeOfCreating').first()
        if debt:
            total_global_debt += debt.debt
    
    return render(request, 'drivers/kamoTables.html', {
        'Tables': tables,
        'CompleteRows': complete_row,
        "table" : join_page_obj,

        'joinedDebt': debt_array,
        'Returned': total_payments_returned,
        'Salary': total_payments_salary,
        'Money': total_payments_money,
        'GlobalDebt': total_global_debt,
        'OldDebt': old_debt,
        'NewDebt': new_debt,
    })



def ohan(request):
    usersArray = [
        'Օհան',
        'Գ.4-րդ',
        'Գ.ավագ',
        'Արա'
    ]
    for i, v in enumerate(usersArray):
        usersArray[i] = User.objects.get(username = v)

    itemsObjects = {
        'ohan':[],
        'gavar':[],
        'avag':[],
        'ara':[]
    }

    for user, us in zip(usersArray, itemsObjects):
        itemsObjects[us] = ItemsModel.objects.filter(customer=user.username)
    
    Items = []
    uniq = ItemsModel.productsfor_Customer(request.user)

    for prod,ohan,gavar,avag,ara in zip(uniq,itemsObjects['ohan'], itemsObjects['gavar'], itemsObjects['avag'], itemsObjects['ara']
        ):
        Items.append(
            [
                prod.productName,
                ohan,
                gavar,
                avag,
                ara
            ]
        )
    # joinedTables = User.objects.filter(is_supplier=True, username__in=["Կիրովական", "Արտադրամաս", "Փուռ"])
    # suppliers = User.objects.filter(is_supplier=True).exclude(username__in=joinedTables.values('username')) 
    # print(Items)
    return render(request, 'drivers/ohan.html', {
        'Items': Items
        # 'Tables': tablesUsers,
        # 'TableRows': tableRows,
        # 'Suppliers': suppliers,
        # "joinedSuppliers": joinedTables
    })

def ohanTables(request):
    page_number = request.GET.get('page')
    # Joined Tables
    ohan_User = request.user
    joinedTables = JoinedTables.objects.filter(
        customer=ohan_User,
        ).order_by('timeOfCreating')  # Reverse the order by '-id'
    joinPaginator = Paginator(joinedTables, 5)  # show 5 joinedTables per page
    join_page_obj = joinPaginator.get_page(page_number)
    reversed_join_page_obj = joinPaginator.get_page(
            joinPaginator.num_pages - join_page_obj.number + 1
        ).__reversed__()  # Reversed join_page_obj
    customers = [
        User.objects.get(username='Օհան'), User.objects.get(username='Գ.4-րդ'),
        User.objects.get(username='Գ.ավագ'), User.objects.get(username='Արա')
        ]

    tables = []

    joinedTables_array = []
    for ohan_join in reversed_join_page_obj:
        mini_arr = []
        tables.append(ohan_join)
        for join in JoinedTables.objects.filter(dateOfCreating = ohan_join.dateOfCreating, customer__in = customers):
            mini_arr.append(join)
        joinedTables_array.append(mini_arr)
    
    joined_Max = []
    for i in joinedTables_array:
        for j in i:
            joined_Max.append(j)

    userTables = UserTable.objects.filter(joinedTable__in = joined_Max)
    userTables_array = []
    for us in userTables:
        userTables_array.append(us)

    suppliers = ['Արտադրամաս','Փուռ','Կիրովական']
    uniq = ItemsModel.productsfor_Customer(ohan_User)
    rows = []
    for joined_arr in joinedTables_array:
        mini_rows = []
        # print(joined_arr)
        for joinedTable in joined_arr:
            table_Rows = []
            for userTable in userTables_array:
                if userTable.joinedTable == joinedTable:
                    for product in uniq:
                        if product.supplier in suppliers:
                            try:
                                if joinedTable.customer.username == 'Օհան':
                                    us = 'ohan'
                                elif joinedTable.customer.username == 'Գ.4-րդ':
                                    us = 'gavar'
                                elif joinedTable.customer.username == 'Գ.ավագ':
                                    us = "avag"
                                elif joinedTable.customer.username == 'Արա':
                                    us = 'ara'
                                r = {
                                    'productName': product.productName, 
                                    us: TableItem.objects.get(
                                        table=userTable,
                                        product_name=product.productName,
                                        customer=joinedTable.customer
                                )}
                                table_Rows.append(r)
                            except:
                                pass
            if joinedTable.customer.username == 'Օհան':
                ts = 'ohan'
            elif joinedTable.customer.username == 'Գ.4-րդ':
                ts = 'gavar'
            elif joinedTable.customer.username == 'Գ.ավագ':
                ts = "avag"
            elif joinedTable.customer.username == 'Արա':
                ts = 'ara'                    
            mini_rows.append({
                'table_name': f'{joinedTable.tableName}',
                ts : table_Rows
                })
        rows.append(mini_rows)

    complete_row = []

    for tab in tables:
        mini_comp = []
        ohan_total = 0
        gavar_total = 0
        avag_total = 0
        ara_total = 0
        big_total = 0
        for row in rows:
            # print(row[3]['ohan'])

            if row[3]['table_name'] == tab.tableName:
                for prod in uniq:
                    row_list = []
                    total_of_row = 0
                    row_list.append(prod.productName)
                        # print(ohan)
                    for ohan in row[3]['ohan']:
                        if ohan['productName'] == prod.productName:
                            row_list.append(ohan['ohan'])
                            total_of_row += ohan['ohan'].total_price
                            ohan_total += ohan['ohan'].total_price
                            break
                    for gavar in row[2]['gavar']:
                        if gavar['productName'] == prod.productName:
                            row_list.append(gavar['gavar'])
                            total_of_row += gavar['gavar'].total_price
                            gavar_total += gavar['gavar'].total_price
                            break
                    for avag in row[1]['avag']:
                        if avag['productName'] == prod.productName:
                            row_list.append(avag['avag'])
                            total_of_row += avag['avag'].total_price
                            avag_total += avag['avag'].total_price
                            break
                    for ara in row[0]['ara']:
                        if ara['productName'] == prod.productName:
                            row_list.append(ara['ara'])
                            total_of_row += ara['ara'].total_price
                            ara_total += ara['ara'].total_price
                            break
                    row_list.append(total_of_row)
                    big_total += total_of_row
                    mini_comp.append(row_list)

                # print(mini_comp)
        complete_row.append({f'{tab.tableName}':mini_comp,'last_row': ['Ընդ', ohan_total, gavar_total, avag_total, ara_total, big_total]})        

    joineddebt = Debt.objects.filter(
        customer = User.objects.get(username = "Օհան"),
        joined = True
        ).order_by('timeOfCreating')
    joineddebtPaginator = Paginator(joineddebt, 5) #show 5 debts per page of the joined tables
    joineddebt_page_obj = joineddebtPaginator.get_page(page_number)
    reversed_joined_debt_obj = joineddebtPaginator.get_page(
        joineddebtPaginator.num_pages - joineddebt_page_obj.number + 1
    )
    single_debt_array = []
    single_debt_dict = {}
    for i in reversed_joined_debt_obj:
        try: 
            singleDebt = Debt.objects.filter(
                single=True, 
                date=i.date,
                customer__in=customers
                )
            if singleDebt[0].date not in single_debt_array:
                single_debt_array.append(singleDebt[0].date)
                single_debt_dict[str(i.date)] = singleDebt.aggregate(sum = Sum('debt'))['sum']
        except:
            continue
    debt_array = []
    for debt in reversed_joined_debt_obj:
        joinTable_debt = Debt.objects.filter(
            joined = True,
            date = debt.date,
            customer__in=customers
        )
        try:
            debt_array.append([str(debt.date),joinTable_debt.aggregate(sum = Sum('debt'))['sum'], single_debt_dict[str(debt.date)]])
        except:
            debt_array.append([str(debt.date),joinTable_debt.aggregate(sum = Sum('debt'))['sum'], ''])
    # PAYMANT
    try:
        total_payments_money = Paymant.objects.filter(
            date = single_debt_array[0],
        ).aggregate(money=models.Sum('money'))['money']
        total_payments_returned = Paymant.objects.filter(
            date = single_debt_array[0],
        ).aggregate(returned=models.Sum('returned'))['returned']
        total_payments_salary = Paymant.objects.filter(
            date = single_debt_array[0],
        ).aggregate(salary=models.Sum('salary'))['salary']
    except:
        total_payments_money = 0
        total_payments_returned = 0
        total_payments_salary = 0

    total_global_debt = 0
    try:
        old_debt = Old_debt.objects.filter(date = single_debt_array[0], customer__in=customers).aggregate(sum = Sum('debt'))['sum']
        new_debt = Week_debt.objects.filter(date = single_debt_array[0], customer__in=customers).aggregate(sum = Sum('debt'))['sum']
    except:
        old_debt = 0
        new_debt = 0
        pass
    for customer in customers:
        debt = Global_Debt.objects.filter(customer=customer).order_by('-timeOfCreating').first()
        if debt:
            total_global_debt += debt.debt

    return render(request, 'drivers/ohanTables.html', {
        'Tables': tables,
        'CompleteRows': complete_row,
        "table" : join_page_obj,

        'joinedDebt': debt_array,
        'Returned': total_payments_returned,
        'Salary': total_payments_salary,
        'Money': total_payments_money,
        'GlobalDebt': total_global_debt,
        'OldDebt': old_debt,
        'NewDebt': new_debt,
    })

@customer_required
def customer(request):
    if request.user.username == 'Կամո':
        return redirect('kamo')
    elif request.user.username == 'Օհան':
        return redirect('ohan')   
    # tablesUsers = UserTable.objects.all()
    items = ItemsModel.productsfor_Customer(request.user)
    # tableRows = TableItem.objects.all()
    joinedTables = User.objects.filter(is_supplier=True, username__in=["Կիրովական", "Արտադրամաս", "Փուռ"])
    suppliers = User.objects.filter(is_supplier=True).exclude(username__in=joinedTables.values('username')) 

    return render(request, 'customer.html', {
        'Items': items,
        # 'Tables': tablesUsers,
        # 'TableRows': tableRows,
        'Suppliers': suppliers,
        "joinedSuppliers": joinedTables
        })


@customer_required
def tablesByUser(request):

    if request.user.username == 'Օհան':
        return redirect('ohanTables')    
    elif request.user.username == 'Կամո':
        return redirect('kamoTables')

    page_number = request.GET.get('page')
    # Joined Tables
    joinedTables = JoinedTables.objects.filter(
        customer=request.user,
        ).order_by('timeOfCreating')  # Reverse the order by '-id'
    joinPaginator = Paginator(joinedTables, 5)  # show 5 joinedTables per page
    join_page_obj = joinPaginator.get_page(page_number)
    reversed_join_page_obj = joinPaginator.get_page(
            joinPaginator.num_pages - join_page_obj.number + 1
        ).__reversed__()  # Reversed join_page_obj
    reversed_join_page_copy = joinPaginator.get_page(
            joinPaginator.num_pages - join_page_obj.number + 1
        ).__reversed__()  # Reversed join_page_obj
    reversed_join_page_for_debt = joinPaginator.get_page(
            joinPaginator.num_pages - join_page_obj.number + 1
        )  # Reversed join_page_obj


    reversed_table_page_obj = []
    for join in reversed_join_page_copy:
        try:
            joins = UserTable.objects.filter(
                user = request.user,
                joinedTable = join,
            )
            for jo in joins:
                reversed_table_page_obj.append(jo)
        except:
            continue
    JoinRows = []
    for tab in reversed_table_page_obj:
        try:
            row =  TableItem.objects.filter(
                customer = request.user,
                table = tab
            )
            for r in row:
                JoinRows.append(r)
        except:
            continue
    
    # Joined Tables

    single_debt_array = []
    debt_array = []
    for i in reversed_join_page_for_debt:
        try:
            joinedDebt = Debt.objects.get(
                customer = request.user,
                joined = True,
                date = i.dateOfCreating
            )
            theDebt = [str(i.dateOfCreating),joinedDebt.debt,""]
            try:
                singleDebt = Debt.objects.get(
                    customer = request.user,
                    single=True, 
                    date=i.dateOfCreating
                    )
                if singleDebt.date not in single_debt_array:
                    single_debt_array.append(singleDebt.date)
                theDebt[2] = singleDebt.debt
            except:
                pass
            debt_array.append(theDebt)
        except:
            continue

    SingleTables = []
    for date in single_debt_array:
        try:
            singleTab = UserTable.objects.get(
                user= request.user,
                singleTable__isnull = False,
                dateOfCreating = date
            )
            SingleTables.append(singleTab)
        except:
            continue

    SingleRows = []
    for table in SingleTables:
        try:
            row = TableItem.objects.filter(
                customer = request.user,
                table = table,
            )
            for r in row:
                SingleRows.append(r)
        except:
            continue
    # Single Tables 
    try:
        weekPaymant = Paymant.objects.get(
            customer = request.user,
            date = single_debt_array[0]
        )
    except:
        weekPaymant = Paymant.objects.none()
    
    try:
        week_debt = Week_debt.objects.get(
            customer = request.user,
            date = single_debt_array[0]
        )
    except:
        week_debt = Week_debt.objects.none()
    
    try:
        old_debt = Old_debt.objects.get(
            customer = request.user,
            date = single_debt_array[0]
        )
    except:
        old_debt = Old_debt.objects.none()

    try:
        globalDebt = Global_Debt.objects.filter(customer = request.user).latest('timeOfCreating')
    except:
        globalDebt = Global_Debt.objects.none()

    try: 
        defaultDate = single_debt_array[0].strftime("%Y-%m-%d")
    except:
        defaultDate = datetime.now().strftime("%Y-%m-%d")
    is_waiting = len(WaitingForChange.objects.filter(customer=request.user)) != 0
    return render(request, 'tablesbyUser.html', {
        'table': join_page_obj,
        'defaultDate': defaultDate,
        'tables': reversed_table_page_obj,
        'joins': reversed_join_page_obj,
        # 'Rows': tableRows,
        "SingleRows": SingleRows ,
        "JoinRows": JoinRows ,

        # 'singleTables': reversed_single_page_obj,
        'singleTables': SingleTables,
        'joinedDebt': debt_array,
        # 'singleDebt': reversed_single_debt_obj,
        'weekPaymant': weekPaymant,
        'weekDebt': week_debt,
        'oldDebt': old_debt,
        'globalDebt': globalDebt,
        'is_waiting': is_waiting
    })

@customer_required
def mistakes(request, table_id):
    # kara vtangavor lini ete idnery hamnknen
    try:
        table = UserTable.objects.get(id = table_id)
        rows = TableItem.objects.filter(table=table)
        context = {
            'table_id': table_id,
            'table': table,
            'rows': rows,
            'is_joined': False,
        }
    except:
        table = JoinedTables.objects.get(id = table_id)
        mid = [TableItem.objects.filter(table = tab) for tab in UserTable.objects.filter(joinedTable = table)]
        rows = []
        for tab in mid:
            for i in tab:
                rows.append(i)
        context = {
            'table_id': table_id,
            'table': table,
            'rows': rows,
            'is_joined': True,
        }
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        # print(data)
        for item in data:
            table_item = TableItem.objects.get(id=item["product_id"])
            if table_item.table.joinedTable:
                WaitingForChange.objects.create(
                    table_item=table_item,
                    newTotal=item['total_price'],
                    newCount=item['product_count'],
                    customer=request.user,
                    date=table_item.table.joinedTable.dateOfCreating
                )
            else:
                WaitingForChange.objects.create(
                    table_item=table_item,
                    newTotal=item['total_price'],
                    newCount=item['product_count'],
                    customer=request.user,
                    date=table_item.table.singleTable.dateOfCreating
                )
        changeList = WaitingForChange.objects.all()
        # print(len(changeList))
        # return HttpResponseRedirect('/account/changes')

    return render(request, 'mistakes.html', context)

@customer_required
def change(request):
    rows = WaitingForChange.objects.filter(customer=request.user)
    return render(request, 'changes.html', {'rows': rows})

@login_required
def delChange(request, item_id):
    item = WaitingForChange.objects.get(id=item_id)
    item.delete()
    if request.user.is_customer:
        return HttpResponseRedirect('/account/changes')
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# ========================== Customer End  ===================

# ////////////////////////// Employee Start //////////////////

@employee_required
def employee(request):
    # tableRows = BigTableRows.objects.all()
    # bigTables = BigTable.objects.all()
    # suppliers = User.objects.filter(is_supplier=True)
    # uniq = ItemsModel.uniqueProductNames(None)
    is_waiting = len(WaitingForChange.objects.all()) != 0
    # uniq = ItemsModel.uniqueProductNames(None)
    # ohanUser = User.objects.get(username='Սարուխան')
    # custItems = ItemsModel.productsfor_Customer(ohanUser)
    # mylist = []
    # for i in uniq:
    #     if i['supplier'] != "Այլ.ապրանք":
    #         mylist.append(i)
    # arrayItem = []
    # for k in custItems:
    #     arrayItem.append(k.productName)

    # for i in mylist:
    #     if i['productName'] not in arrayItem:
    #         ItemsModel.objects.create(
    #             customer = 'Սարուխան',
    #             supplier = i['supplier'],
    #             productName = i['productName'],
    #             productPrice = 0,
    #             supPrice = 0
    #         )

    return render(request, 'employee.html', {
        # 'Products': uniq,
        # 'TableRows': tableRows,
        # 'BigTables': bigTables,
        # 'Suppliers': suppliers,
        'is_waiting': is_waiting
    })


@employee_required
def otherItems(request):
    supplier = User.objects.get(username='Այլ.ապրանք')
    tableRows = BigTableRows.objects.filter(supplier=supplier)
    bigTables = BigTable.objects.filter(supplier=supplier)
    is_waiting = len(WaitingForChange.objects.all()) != 0
    uniq = ItemsModel.uniqueProductNames(None).filter(supplier='Այլ.ապրանք')
    return render(
        request,
        "otherItems.html",
        {
            'Products': uniq,
            'TableRows': tableRows,
            'BigTables': bigTables,
            'supplier': supplier,
            'is_waiting': is_waiting
        }
                  )

@employee_required
def mainItems(request): 
    uniq = ItemsModel.uniqueProductNames(None).filter(supplier__in=['Արտադրամաս', 'Փուռ','Կիրովական'])
    suppliers = []
    for i in ['Արտադրամաս','Փուռ','Կիրովական']:
        suppliers.append(User.objects.get(username=i))
    tableRows = BigTableRows.objects.filter(supplier__in=suppliers)
    bigTables = BigTable.objects.filter(supplier__in=suppliers)
    is_waiting = len(WaitingForChange.objects.all()) != 0
    # us = User.objects.get(username='60')
    # bs = User.objects.get(username='148')
    # ds = User.objects.get(username='104')
    # for i,j,g in zip(BigTableRows.objects.filter(user=ds),BigTableRows.objects.filter(user=bs),BigTableRows.objects.filter(user=us)):
    #     print(i,j,g,'aaa')
    # print(TableItem.objects.filter(product_name='Բուլկի կաթ'))
    # for i in [
    # '148', '44',
    # '171', '136',
    # '177', '48',
    # '87', '93',
    # '117', '188',
    # '90', '60',
    # '104', '170',
    # '54', '189',
    # ]:
    #     us = User.objects.get(username=i)
    #     if i == '60':
    #         for i in BigTableRows.objects.filter(user=us):
    #             print(i.item.product_name)
        
    return render(
        request,
        "mainItems.html",
        {
            'Products': uniq,
            'TableRows': tableRows,
            'BigTables': bigTables,
            'Suppliers': suppliers,
            'is_waiting': is_waiting
        }
                  )

@employee_required
def allCustomers(request):
    allCustomers = User.objects.filter(is_customer = True)
    allSuppliers = User.objects.filter(is_supplier = True)
    globDebts = []
    for cust in allCustomers:
        try:
            latest_global = Global_Debt.objects.filter(customer=cust).latest('timeOfCreating')
            globDebts.append([cust, latest_global.debt, len(WaitingForChange.objects.filter(customer=cust)) != 0])
            # print(cust.id)
        except:
            globDebts.append([cust, 0, len(WaitingForChange.objects.filter(customer=cust)) != 0])

    ohanDebt = 0
    kamoDebt = 0

    ohan_Users = ['Օհան','Գ.4-րդ', 'Գ.ավագ', 'Արա']
    kamo_Users = ['Կամո', 'Գանձակ', 'Սարուխան']

    for username in ohan_Users:
        user = User.objects.get(username=username)
        try:
            latest_global = Global_Debt.objects.filter(customer=user).latest('timeOfCreating')
            ohanDebt += latest_global.debt

        except:
            pass

    for username in kamo_Users:
        user = User.objects.get(username=username)
        try:
            latest_global = Global_Debt.objects.filter(customer=user).latest('timeOfCreating')
            kamoDebt += latest_global.debt
        except:
            pass
    
    return render(request, 'work.html',{
        'allCustomers':allCustomers,
        'debts': globDebts,
        'allSuppliers': allSuppliers,
        'ohanDebt': ohanDebt,
        'kamoDebt': kamoDebt,

    })

@employee_required
def endorse(request, user_id):
    page_user = User.objects.get(id=user_id)
    rows = WaitingForChange.objects.filter(customer=page_user)
    return render(request, 'endorse.html', {'rows': rows, 'page_user':page_user})


@employee_required
def endorseChange(request, item_id):
    item = TableItem.objects.get(id=item_id)
    tochange_item = WaitingForChange.objects.get(table_item=item)
    try:
        sup_price = item.supTotal / item.product_count
    except:
        sup_price = 0
    difference = item.total_price - tochange_item.newTotal
    latest_global_debt = Global_Debt.objects.filter(customer=tochange_item.customer).latest('timeOfCreating')
    Global_Debt.objects.create(
        customer = tochange_item.customer,
        date = tochange_item.date,
        debt = latest_global_debt.debt - difference,
    )

    if tochange_item.table_item.table.joinedTable:
        tochange_debt = Debt.objects.get(
            date=tochange_item.date,
            customer=tochange_item.customer,
            joined=True,
        )
    else:
        tochange_debt = Debt.objects.get(
            date=tochange_item.date,
            customer=tochange_item.customer,
            single=True,
        )
    tochange_debt.debt -= difference
    tochange_debt.save()


    item.product_count = tochange_item.newCount
    item.total_price = tochange_item.newTotal
    item.supTotal = tochange_item.newCount * sup_price
    item.save()
    tochange_item.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@employee_required
def customerTables(request, user_id):
    user = User.objects.get(id=user_id)
    page_number = request.GET.get('page')
    # Joined Tables
    joinedTables = JoinedTables.objects.filter(
        customer=user,
    ).order_by('timeOfCreating')  # Reverse the order by '-id'
    joinPaginator = Paginator(joinedTables, 5)  # show 5 joinedTables per page
    join_page_obj = joinPaginator.get_page(page_number)
    reversed_join_page_obj = joinPaginator.get_page(
        joinPaginator.num_pages - join_page_obj.number + 1
    ).__reversed__()  # Reversed join_page_obj
    reversed_join_page_copy = joinPaginator.get_page(
        joinPaginator.num_pages - join_page_obj.number + 1
    ).__reversed__()  # Reversed join_page_obj
    reversed_join_page_for_debt = joinPaginator.get_page(
        joinPaginator.num_pages - join_page_obj.number + 1
    )  # Reversed join_page_obj
    reversed_table_page_obj = []
    for join in reversed_join_page_copy:
        try:
            joins = UserTable.objects.filter(
                user=user,
                joinedTable=join,
            )
            for jo in joins:
                reversed_table_page_obj.append(jo)
        except:
            continue
    JoinRows = []
    for tab in reversed_table_page_obj:
        try:
            row = TableItem.objects.filter(
                customer=user,
                table=tab
            )
            for r in row:
                JoinRows.append(r)
        except:
            continue
    # Joined Tables
    single_debt_array = []
    debt_array = []
    for i in reversed_join_page_for_debt:
        try:
            joinedDebt = Debt.objects.get(
                customer=user,
                joined=True,
                date=i.dateOfCreating
            )
            theDebt = [str(i.dateOfCreating), joinedDebt.debt, ""]
            try:
                singleDebt = Debt.objects.get(
                    customer=user,
                    single=True,
                    date=i.dateOfCreating
                )
                if singleDebt.date not in single_debt_array:
                    single_debt_array.append(singleDebt.date)
                theDebt[2] = singleDebt.debt
            except:
                pass
            debt_array.append(theDebt)
        except:
            continue

    SingleTables = []
    for date in single_debt_array:
        try:
            singleTab = UserTable.objects.get(
                user=user,
                singleTable__isnull=False,
                dateOfCreating=date
            )
            SingleTables.append(singleTab)
        except:
            continue
    SingleRows = []
    for table in SingleTables:
        try:
            row = TableItem.objects.filter(
                customer=user,
                table=table,
            )
            for r in row:
                SingleRows.append(r)
        except:
            continue
    # Single Tables
    try:
        weekPaymant = Paymant.objects.get(
            customer=user,
            date=single_debt_array[0]
        )
    except:
        weekPaymant = Paymant.objects.none()

    try:
        week_debt = Week_debt.objects.get(
            customer=user,
            date=single_debt_array[0]
        )
    except:
        week_debt = Week_debt.objects.none()

    try:
        old_debt = Old_debt.objects.get(
            customer=user,
            date=single_debt_array[0]
        )
    except:
        old_debt = Old_debt.objects.none()

    try:
        globalDebt = Global_Debt.objects.filter(customer=user).latest('timeOfCreating')
    except:
        globalDebt = Global_Debt.objects.none()

    try:
        defaultDate = single_debt_array[0].strftime("%Y-%m-%d")
    except:
        defaultDate = datetime.now().strftime("%Y-%m-%d")

    return render(request, 'customerTables.html', {
        'table': join_page_obj,
        'defaultDate': defaultDate,
        'tables': reversed_table_page_obj,
        'joins': reversed_join_page_obj,
        # 'Rows': tableRows,
        "SingleRows": SingleRows,
        "JoinRows": JoinRows,
        # 'singleTables': reversed_single_page_obj,
        'singleTables': SingleTables,
        'joinedDebt': debt_array,
        # 'singleDebt': reversed_single_debt_obj,
        'weekPaymant': weekPaymant,
        'weekDebt': week_debt,
        'oldDebt': old_debt,
        'globalDebt': globalDebt,
        'customer': user
    })

# import time
def myOrders(request, supplier_id):
    # start = time.time()
    schools = ['148', '189', '54', '170', '104', '136', '171', '117', '177', '48', '60', 'Օհան', 
            'Գ.4-րդ', 'Գ.ավագ', 'Արա', 'Կամո', 'Գանձակ', 'Սարուխան', 'Էրանոս',
            'Լիճք', 'Մ.1ին', 'Զոլ.2րդ', 'Զոլ.1ին'
            ]
    theSupplier = User.objects.get(id = supplier_id)
    orderedProducts_Tables = Ordered_Products_Table.objects.filter(supplierof_Table = theSupplier)
    paginator = Paginator(orderedProducts_Tables, 2) # show 3 tables per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    uniq = ItemsModel.uniqueProductNames(theSupplier)
    customers = User.objects.filter(is_customer = True)
    school_order = {school: i for i, school in enumerate(schools)}
    arrFromColums = []
    arrFromOrdTabs = []
    kamo_User = User.objects.get(username='Կամո')
    ohan_User = User.objects.get(username='Օհան')

    for tab in page_obj:
        if tab not in arrFromOrdTabs:
            arrFromOrdTabs.append(tab)

    columns_OFtable = Ordered_Products_Column.objects.filter(
        supplierof_table = theSupplier
        ).filter(
            parent_Table__in = arrFromOrdTabs
        )

    for j in columns_OFtable:
        if j not in arrFromColums:
            arrFromColums.append(j.table)

    tableRows = (TableItem.objects.filter(supplier_id = supplier_id).filter(
        table__in=arrFromColums
    ) | TableItem.objects.filter(
        customer__in = [kamo_User,ohan_User],
        table__in=arrFromColums
    ))

    sorted_columns = sorted(columns_OFtable, key=lambda col: school_order.get(col.table.user.username, len(schools)))
    
    # end = time.time()

    # print(end-start, tableRows.count())
    return render(request, 'myOrders.html', {
        'supplier': theSupplier,
        'Tables': page_obj,
        'Columns_of_Table': sorted_columns,
        'Products': uniq,
        'Customers': customers,
        'TableRows': tableRows,
    })

def tables_by_ohan(request):
    page_number = request.GET.get('page')
    # Joined Tables
    ohan_User = User.objects.get(username='Օհան')
    joinedTables = JoinedTables.objects.filter(
        customer=ohan_User,
        ).order_by('timeOfCreating')  # Reverse the order by '-id'
    joinPaginator = Paginator(joinedTables, 5)  # show 5 joinedTables per page
    join_page_obj = joinPaginator.get_page(page_number)
    reversed_join_page_obj = joinPaginator.get_page(
            joinPaginator.num_pages - join_page_obj.number + 1
        ).__reversed__()  # Reversed join_page_obj
    customers = [
        User.objects.get(username='Օհան'), User.objects.get(username='Գ.4-րդ'),
        User.objects.get(username='Գ.ավագ'), User.objects.get(username='Արա')
        ]

    tables = []

    joinedTables_array = []
    for ohan_join in reversed_join_page_obj:
        mini_arr = []
        tables.append(ohan_join)
        for join in JoinedTables.objects.filter(dateOfCreating = ohan_join.dateOfCreating, customer__in = customers):
            mini_arr.append(join)
        joinedTables_array.append(mini_arr)
    
    joined_Max = []
    for i in joinedTables_array:
        for j in i:
            joined_Max.append(j)

    userTables = UserTable.objects.filter(joinedTable__in = joined_Max)
    userTables_array = []
    for us in userTables:
        userTables_array.append(us)

    suppliers = ['Արտադրամաս','Փուռ','Կիրովական']
    uniq = ItemsModel.productsfor_Customer(ohan_User)
    rows = []
    for joined_arr in joinedTables_array:
        mini_rows = []
        # print(joined_arr)
        for joinedTable in joined_arr:
            table_Rows = []
            for userTable in userTables_array:
                if userTable.joinedTable == joinedTable:
                    for product in uniq:
                        if product.supplier in suppliers:
                            try:
                                if joinedTable.customer.username == 'Օհան':
                                    us = 'ohan'
                                elif joinedTable.customer.username == 'Գ.4-րդ':
                                    us = 'gavar'
                                elif joinedTable.customer.username == 'Գ.ավագ':
                                    us = "avag"
                                elif joinedTable.customer.username == 'Արա':
                                    us = 'ara'
                                r = {
                                    'productName': product.productName, 
                                    us: TableItem.objects.get(
                                        table=userTable,
                                        product_name=product.productName,
                                        customer=joinedTable.customer
                                )}
                                table_Rows.append(r)
                            except:
                                pass
            if joinedTable.customer.username == 'Օհան':
                ts = 'ohan'
            elif joinedTable.customer.username == 'Գ.4-րդ':
                ts = 'gavar'
            elif joinedTable.customer.username == 'Գ.ավագ':
                ts = "avag"
            elif joinedTable.customer.username == 'Արա':
                ts = 'ara'                    
            mini_rows.append({
                'table_name': f'{joinedTable.tableName}',
                ts : table_Rows
                })
        rows.append(mini_rows)

    complete_row = []

    for tab in tables:
        mini_comp = []
        ohan_total = 0
        gavar_total = 0
        avag_total = 0
        ara_total = 0
        big_total = 0
        for row in rows:
            # print(row[3]['ohan'])

            if row[3]['table_name'] == tab.tableName:
                for prod in uniq:
                    row_list = []
                    total_of_row = 0
                    row_list.append(prod.productName)
                        # print(ohan)
                    for ohan in row[3]['ohan']:
                        if ohan['productName'] == prod.productName:
                            row_list.append(ohan['ohan'])
                            total_of_row += ohan['ohan'].total_price
                            ohan_total += ohan['ohan'].total_price
                            break
                    for gavar in row[2]['gavar']:
                        if gavar['productName'] == prod.productName:
                            row_list.append(gavar['gavar'])
                            total_of_row += gavar['gavar'].total_price
                            gavar_total += gavar['gavar'].total_price
                            break
                    for avag in row[1]['avag']:
                        if avag['productName'] == prod.productName:
                            row_list.append(avag['avag'])
                            total_of_row += avag['avag'].total_price
                            avag_total += avag['avag'].total_price
                            break
                    for ara in row[0]['ara']:
                        if ara['productName'] == prod.productName:
                            row_list.append(ara['ara'])
                            total_of_row += ara['ara'].total_price
                            ara_total += ara['ara'].total_price
                            break
                    row_list.append(total_of_row)
                    big_total += total_of_row
                    mini_comp.append(row_list)

                # print(mini_comp)
        complete_row.append({f'{tab.tableName}':mini_comp,'last_row': ['Ընդ', ohan_total, gavar_total, avag_total, ara_total, big_total]})        

    joineddebt = Debt.objects.filter(
        customer = User.objects.get(username = "Օհան"),
        joined = True
        ).order_by('timeOfCreating')
    joineddebtPaginator = Paginator(joineddebt, 5) #show 5 debts per page of the joined tables
    joineddebt_page_obj = joineddebtPaginator.get_page(page_number)
    reversed_joined_debt_obj = joineddebtPaginator.get_page(
        joineddebtPaginator.num_pages - joineddebt_page_obj.number + 1
    )
    single_debt_array = []
    single_debt_dict = {}
    for i in reversed_joined_debt_obj:
        try: 
            singleDebt = Debt.objects.filter(
                single=True, 
                date=i.date,
                customer__in=customers
                )
            if singleDebt[0].date not in single_debt_array:
                single_debt_array.append(singleDebt[0].date)
                single_debt_dict[str(i.date)] = singleDebt.aggregate(sum = Sum('debt'))['sum']
        except:
            continue
    debt_array = []
    for debt in reversed_joined_debt_obj:
        joinTable_debt = Debt.objects.filter(
            joined = True,
            date = debt.date,
            customer__in=customers
        )
        try:
            debt_array.append([str(debt.date),joinTable_debt.aggregate(sum = Sum('debt'))['sum'], single_debt_dict[str(debt.date)]])
        except:
            debt_array.append([str(debt.date),joinTable_debt.aggregate(sum = Sum('debt'))['sum'], ''])
    # PAYMANT
    try:
        total_payments_money = Paymant.objects.filter(
            date = single_debt_array[0],
        ).aggregate(money=models.Sum('money'))['money']
        total_payments_returned = Paymant.objects.filter(
            date = single_debt_array[0],
        ).aggregate(returned=models.Sum('returned'))['returned']
        total_payments_salary = Paymant.objects.filter(
            date = single_debt_array[0],
        ).aggregate(salary=models.Sum('salary'))['salary']
    except:
        total_payments_money = 0
        total_payments_returned = 0
        total_payments_salary = 0

    total_global_debt = 0
    try:
        old_debt = Old_debt.objects.filter(date = single_debt_array[0], customer__in=customers).aggregate(sum = Sum('debt'))['sum']
        new_debt = Week_debt.objects.filter(date = single_debt_array[0], customer__in=customers).aggregate(sum = Sum('debt'))['sum']
    except:
        old_debt = 0
        new_debt = 0
        pass
    for customer in customers:
        debt = Global_Debt.objects.filter(customer=customer).order_by('-timeOfCreating').first()
        if debt:
            total_global_debt += debt.debt

    return render(request, 'drivers/tablesBYohan.html', {
        'Tables': tables,
        'CompleteRows': complete_row,
        "table" : join_page_obj,

        'joinedDebt': debt_array,
        'Returned': total_payments_returned,
        'Salary': total_payments_salary,
        'Money': total_payments_money,
        'GlobalDebt': total_global_debt,
        'OldDebt': old_debt,
        'NewDebt': new_debt,
    })

def tables_by_kamo(request):

    page_number = request.GET.get('page')
    # Joined Tables
    kamo_User = User.objects.get(username='Կամո')
    joinedTables = JoinedTables.objects.filter(
        customer=kamo_User,
        ).order_by('timeOfCreating')  # Reverse the order by '-id'
    joinPaginator = Paginator(joinedTables, 5)  # show 5 joinedTables per page
    join_page_obj = joinPaginator.get_page(page_number)
    reversed_join_page_obj = joinPaginator.get_page(
            joinPaginator.num_pages - join_page_obj.number + 1
        ).__reversed__()  # Reversed join_page_obj
    customers = [
        User.objects.get(username='Կամո'),
        User.objects.get(username='Գանձակ'),
        User.objects.get(username='Սարուխան')
        ]

    tables = []

    joinedTables_array = []
    for ohan_join in reversed_join_page_obj:
        mini_arr = []
        tables.append(ohan_join)
        for join in JoinedTables.objects.filter(dateOfCreating = ohan_join.dateOfCreating, customer__in = customers):
            mini_arr.append(join)
        joinedTables_array.append(mini_arr)
    
    joined_Max = []
    for i in joinedTables_array:
        for j in i:
            joined_Max.append(j)

    userTables = UserTable.objects.filter(joinedTable__in = joined_Max)
    userTables_array = []
    for us in userTables:
        userTables_array.append(us)

    suppliers = ['Արտադրամաս','Փուռ','Կիրովական']
    uniq = ItemsModel.productsfor_Customer(kamo_User)
    rows = []
    for joined_arr in joinedTables_array:
        mini_rows = []
        # print(joined_arr)
        for joinedTable in joined_arr:
            table_Rows = []
            for userTable in userTables_array:
                if userTable.joinedTable == joinedTable:
                    for product in uniq:
                        if product.supplier in suppliers:
                            try:
                                if joinedTable.customer.username == 'Կամո':
                                    us = 'kamo'
                                elif joinedTable.customer.username == 'Գանձակ':
                                    us = 'gandak'
                                elif joinedTable.customer.username == 'Սարուխան':
                                    us = "sarukan"
                                r = {
                                    'productName': product.productName, 
                                    us: TableItem.objects.get(
                                        table=userTable,
                                        product_name=product.productName,
                                        customer=joinedTable.customer
                                )}
                                table_Rows.append(r)
                            except:
                                pass
            if joinedTable.customer.username == 'Կամո':
                ts = 'kamo'
            elif joinedTable.customer.username == 'Գանձակ':
                ts = 'gandak'
            elif joinedTable.customer.username == 'Սարուխան':
                ts = "sarukan"             
            mini_rows.append({
                'table_name': f'{joinedTable.tableName}',
                ts : table_Rows
                })
        rows.append(mini_rows)

    complete_row = []

    for tab in tables:
        mini_comp = []
        kamo_total = 0
        gandak_total = 0
        sarukan_total = 0
        big_total = 0
        for row in rows:
            # print(row[3]['ohan'])

            if row[2]['table_name'] == tab.tableName:
                for prod in uniq:
                    row_list = []
                    total_of_row = 0
                    row_list.append(prod.productName)
                        # print(ohan)
                    for kamo in row[2]['kamo']:
                        if kamo['productName'] == prod.productName:
                            row_list.append(kamo['kamo'])
                            total_of_row += kamo['kamo'].total_price
                            kamo_total += kamo['kamo'].total_price
                            break
                    for gandak in row[1]['gandak']:
                        if gandak['productName'] == prod.productName:
                            row_list.append(gandak['gandak'])
                            total_of_row += gandak['gandak'].total_price
                            gandak_total += gandak['gandak'].total_price
                            break
                    for sarukan in row[0]['sarukan']:
                        if sarukan['productName'] == prod.productName:
                            row_list.append(sarukan['sarukan'])
                            total_of_row += sarukan['sarukan'].total_price
                            sarukan_total += sarukan['sarukan'].total_price
                            break
                    row_list.append(total_of_row)
                    big_total += total_of_row
                    mini_comp.append(row_list)

                # print(mini_comp)
        complete_row.append({f'{tab.tableName}':mini_comp,'last_row': ['Ընդ', kamo_total, gandak_total, sarukan_total, big_total]})        

    joineddebt = Debt.objects.filter(
        customer = User.objects.get(username = "Կամո"),
        joined = True
        ).order_by('timeOfCreating')
    joineddebtPaginator = Paginator(joineddebt, 5) #show 5 debts per page of the joined tables
    joineddebt_page_obj = joineddebtPaginator.get_page(page_number)
    reversed_joined_debt_obj = joineddebtPaginator.get_page(
        joineddebtPaginator.num_pages - joineddebt_page_obj.number + 1
    )
    single_debt_array = []
    single_debt_dict = {}
    for i in reversed_joined_debt_obj:
        try: 
            singleDebt = Debt.objects.filter(
                single=True, 
                date=i.date,
                customer__in=customers
                )
            if singleDebt[0].date not in single_debt_array:
                single_debt_array.append(singleDebt[0].date)
                single_debt_dict[str(i.date)] = singleDebt.aggregate(sum = Sum('debt'))['sum']
        except:
            continue
    debt_array = []
    for debt in reversed_joined_debt_obj:
        joinTable_debt = Debt.objects.filter(
            joined = True,
            date = debt.date,
            customer__in=customers
        )
        try:
            debt_array.append([str(debt.date),joinTable_debt.aggregate(sum = Sum('debt'))['sum'], single_debt_dict[str(debt.date)]])
        except:
            debt_array.append([str(debt.date),joinTable_debt.aggregate(sum = Sum('debt'))['sum'], ''])
    # PAYMANT
    try:
        total_payments_money = Paymant.objects.filter(
            date = single_debt_array[0],
        ).aggregate(money=models.Sum('money'))['money']
        total_payments_returned = Paymant.objects.filter(
            date = single_debt_array[0],
        ).aggregate(returned=models.Sum('returned'))['returned']
        total_payments_salary = Paymant.objects.filter(
            date = single_debt_array[0],
        ).aggregate(salary=models.Sum('salary'))['salary']
    except:
        total_payments_money = 0
        total_payments_returned = 0
        total_payments_salary = 0

    total_global_debt = 0
    try:
        old_debt = Old_debt.objects.filter(date = single_debt_array[0], customer__in=customers).aggregate(sum = Sum('debt'))['sum']
        new_debt = Week_debt.objects.filter(date = single_debt_array[0], customer__in=customers).aggregate(sum = Sum('debt'))['sum']
    except:
        old_debt = 0
        new_debt = 0
        pass
    for customer in customers:
        debt = Global_Debt.objects.filter(customer=customer).order_by('-timeOfCreating').first()
        if debt:
            total_global_debt += debt.debt
    
    return render(request, 'drivers/tablesBYkamo.html', {
        'Tables': tables,
        'CompleteRows': complete_row,
        "table" : join_page_obj,

        'joinedDebt': debt_array,
        'Returned': total_payments_returned,
        'Salary': total_payments_salary,
        'Money': total_payments_money,
        'GlobalDebt': total_global_debt,
        'OldDebt': old_debt,
        'NewDebt': new_debt,
    })

@employee_required
def totalPage(request):
    page_number = request.GET.get('page')  
    joineddebt = Debt.objects.filter(
        customer = User.objects.get(username = "171"),
        joined = True
        ).order_by('timeOfCreating')
    joineddebtPaginator = Paginator(joineddebt, 5) #show 5 debts per page of the joined tables
    joineddebt_page_obj = joineddebtPaginator.get_page(page_number)
    reversed_joined_debt_obj = joineddebtPaginator.get_page(
        joineddebtPaginator.num_pages - joineddebt_page_obj.number + 1
    )
    single_debt_array = []
    single_debt_dict = {}
    for i in reversed_joined_debt_obj:
        try: 
            singleDebt = Debt.objects.filter(
                single=True, 
                date=i.date
                )
            if singleDebt[0].date not in single_debt_array:
                single_debt_array.append(singleDebt[0].date)
                single_debt_dict[str(i.date)] = singleDebt.aggregate(sum = Sum('debt'))['sum']
        except:
            continue
    debt_array = []
    for debt in reversed_joined_debt_obj:
        joinTable_debt = Debt.objects.filter(
            joined = True,
            date = debt.date
        )
        try:
            debt_array.append([str(debt.date),joinTable_debt.aggregate(sum = Sum('debt'))['sum'], single_debt_dict[str(debt.date)]])
        except:
            debt_array.append([str(debt.date),joinTable_debt.aggregate(sum = Sum('debt'))['sum'], ''])
    # PAYMANT
    try:
        total_payments_money = Paymant.objects.filter(
            date = single_debt_array[0],
        ).aggregate(money=models.Sum('money'))['money']
        total_payments_returned = Paymant.objects.filter(
            date = single_debt_array[0],
        ).aggregate(returned=models.Sum('returned'))['returned']
        total_payments_salary = Paymant.objects.filter(
            date = single_debt_array[0],
        ).aggregate(salary=models.Sum('salary'))['salary']
    except:
        total_payments_money = 0
        total_payments_returned = 0
        total_payments_salary = 0

    # PAYMANT

    customers = User.objects.filter(is_customer=True)
    total_global_debt = 0
    try:
        old_debt = Old_debt.objects.filter(date = single_debt_array[0]).aggregate(sum = Sum('debt'))['sum']
        new_debt = Week_debt.objects.filter(date = single_debt_array[0]).aggregate(sum = Sum('debt'))['sum']
    except:
        old_debt = 0
        new_debt = 0
        pass
    for customer in customers:
        debt = Global_Debt.objects.filter(customer=customer).order_by('-timeOfCreating').first()
        if debt:
            total_global_debt += debt.debt

    return render(request, 'totalPage.html',{
        'joinedDebt': debt_array,
        'table': joineddebt_page_obj,
        # 'singleDebt': single_debt_by_date,
        'Returned': total_payments_returned,
        'Salary': total_payments_salary,
        'Money': total_payments_money,
        'GlobalDebt': total_global_debt,
        'OldDebt': old_debt,
        'NewDebt': new_debt,
    })

# \\\\\\\\\\\\\\\\\\\\\\\\\\ Employee End   \\\\\\\\\\\\\\\\\\

# ========================== Admin Start    ==================

@admin_required
def admin(request):
    users = User.objects.filter(is_customer=True)
    suppliers = User.objects.filter(is_supplier=True)

    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        # print(data)
        customers = data['customers']
        supplier = data['supplier']
        productName = data['productName']
        productPrice = data['productPrice']
        supPrice = data['supPrice']
        # print('post')
        for customer in customers:
            item = ItemsModel(
                customer=customer,
                supplier=supplier,
                productName=productName,
                productPrice=productPrice,
                supPrice=supPrice
            )
            item.save()

        return redirect('adminpage')
        # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        form = ItemAddForm()

    # items = ItemsModel.objects.all()
    uniq = ItemsModel.uniqueProductNames(None)
    # print(uniq)
    return render(request, 'admin.html', {
        # 'Items': items, 
        'Users': users, 
        'Suppliers': suppliers, 
        'Form': form,
        'Uniq': uniq
        })

@admin_required
def cahngeItemsName(request):
    if request.method == 'POST':
        form = ChangeItemsName(request.POST)
        if form.is_valid():
            from_name = form.cleaned_data['fromName']
            to_name = form.cleaned_data['toName']
            # print(from_name, to_name)
            itemsMod = ItemsModel.objects.filter(productName=from_name)
            tableItems = TableItem.objects.filter(product_name=from_name)
            bigtabRows = BigTableRows.objects.filter(porduct_name=from_name)

            for i in itemsMod:
                i.productName = to_name
                i.save()
            
            for j in tableItems:
                j.product_name = to_name
                j.save()

            for g in bigtabRows:
                g.porduct_name = to_name
                g.save()


            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@admin_required
def delete_item(request, item_id):
    item = get_object_or_404(ItemsModel, id=item_id)
    item.delete()       
    # return redirect('adminpage')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@admin_required
def delete_item_all(request, item_id):
    item = get_object_or_404(ItemsModel, id=item_id)
    item.delete()
    # return redirect('productsforall')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@admin_required
def delete_item_byuser(request, item_id):
    item = get_object_or_404(ItemsModel, id=item_id)
    item.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@admin_required
def edit_item(request, item_id):
    customers = User.objects.filter(is_customer=True)
    item = get_object_or_404(ItemsModel, id=item_id)
    suppliers = User.objects.filter(is_supplier = True)
    if request.method == 'POST':
        form = ItemAddForm(request.POST, instance=item)
        if form.is_valid():
            item = form.save(commit=False)
            item.save()
            return redirect('adminpage')
            # return redirect(request.META.get('HTTP_REFERER'))
    else:
        form = ItemAddForm(instance=item)
    return render(request, 'edit_item.html', {'form': form,'item':item, 'Users': customers, 'Suppliers': suppliers})

@admin_required
def allCustomersforAdmin(request):
    allCustomers = User.objects.filter(is_customer = True)
    return render(request, 'allCustomersforAdmin.html',{'allCustomers':allCustomers})

@admin_required
def customersProducts(request, user_id):
    customer = User.objects.get(id = user_id)
    Products = ItemsModel.objects.all()
    return render(request, 'customerProducts.html', {'customer': customer, 'products':Products})

@admin_required
def productsForAll(request):
    Products = ItemsModel.objects.filter(customer = 'all')
    return render(request, 'productsForAll.html', {'products': Products})

# ========================== Admin End      ==================

# ///////////////////////// Supplier Start  //////////////////
@supplier_required
def supplier(request):
    # schools = ['148', '189', '54', '170', '104', '136', '171', '117', '177', '48', '60', 'Օհան', 
    #            'Գ.4-րդ', 'Գ.ավագ', 'Արա', 'Կամո', 'Գանձակ', 'Սարուխան', 'Էրանոս',
    #            'Լիճք', 'Մ.1ին', 'Զոլ.2րդ', 'Զոլ.1ին'
    #            ]
    # # products = ItemsModel.objects.filter(supplier = request.user.username)
    # orderedProducts_Tables = Ordered_Products_Table.objects.filter(supplierof_Table = request.user)
    # columnsOFtable = Ordered_Products_Column.objects.filter(supplierof_table = request.user)
    # # sorted_columns = columnsOFtable.annotate(
    # #     custom_order=Case(
    # #         *[When(column_name=school, then=Value(i)) for i, school in enumerate(schools)],
    # #         default=Value(len(schools)),
    # #         output_field=IntegerField()
    # #     )
    # # ).order_by('custom_order')

    
    # uniq = ItemsModel.uniqueProductNames(request.user)
    # customers = User.objects.filter(is_customer = True)
    # tableRows = TableItem.objects.filter(supplier=request.user)
    # # print(tableRows.count())

    # paginator = Paginator(orderedProducts_Tables, 5) # show 3 tables per page
    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)

    # return render(request, 'supplier.html', {
    #     'Tables': page_obj,
    #     'Columns_of_Table': columnsOFtable,
    #     'Products': uniq,
    #     'Customers': customers,
    #     'TableRows': tableRows,
    # })
    # start = time.time()
    schools = ['148', '189', '54', '170', '104', '136', '171', '117', '177', '48', '60', 'Օհան', 
            'Գ.4-րդ', 'Գ.ավագ', 'Արա', 'Կամո', 'Գանձակ', 'Սարուխան', 'Էրանոս',
            'Լիճք', 'Մ.1ին', 'Զոլ.2րդ', 'Զոլ.1ին'
            ]
    orderedProducts_Tables = Ordered_Products_Table.objects.filter(supplierof_Table = request.user)
    paginator = Paginator(orderedProducts_Tables, 2) # show 3 tables per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    uniq = ItemsModel.uniqueProductNames(request.user)
    customers = User.objects.filter(is_customer = True)
    school_order = {school: i for i, school in enumerate(schools)}
    arrFromColums = []
    arrFromOrdTabs = []
    kamo_User = User.objects.get(username='Կամո')
    ohan_User = User.objects.get(username='Օհան')

    for tab in page_obj:
        if tab not in arrFromOrdTabs:
            arrFromOrdTabs.append(tab)

    columns_OFtable = Ordered_Products_Column.objects.filter(
        supplierof_table = request.user
        ).filter(
            parent_Table__in = arrFromOrdTabs
        )

    for j in columns_OFtable:
        if j not in arrFromColums:
            arrFromColums.append(j.table)

    tableRows = (TableItem.objects.filter(supplier = request.user).filter(
        table__in=arrFromColums
    ) | TableItem.objects.filter(
        customer__in = [kamo_User,ohan_User],
        table__in=arrFromColums
    ))

    sorted_columns = sorted(columns_OFtable, key=lambda col: school_order.get(col.table.user.username, len(schools)))
    
    # end = time.time()

    print(tableRows.count())
    return render(request, 'supplier.html', {
        'Tables': page_obj,
        'Columns_of_Table': sorted_columns,
        'Products': uniq,
        'Customers': customers,
        'TableRows': tableRows,
    })


@supplier_required
def orderedProducts(request):
    items_list = []
    uniq_lsit = []
    items = ItemsModel.objects.filter(supplier=request.user.username)
    for i in items:
        if i.productName not in uniq_lsit:
            uniq_lsit.append(i.productName)
            items_list.append({'productName': i.productName, 'supPrice': i.supPrice})
    return render(request, 'ordered_Product.html', {'items': items_list})
# \\\\\\\\\\\\\\\\\\\\\\\\ Supplier End     \\\\\\\\\\\\\\\\\\  