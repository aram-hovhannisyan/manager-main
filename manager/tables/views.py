from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect

from .models import (
    ItemsModel,
    TableItem,
    UserTable,
    BigTable,
    Debt,
    Ordered_Products_Column,
    Ordered_Products_Table,
    JoinedTables,
    SingleTable,
    Paymant,
    Global_Debt,
    Week_debt,
    Old_debt,
    BigTableRows
)
from account.models import User

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json

# from datetime import timedelta
from datetime import datetime, timedelta

from django.shortcuts import redirect

from account.forms import PaymantForm

# Create your views here.

yerevan_schools = [
    '148', '44',
    '171', '136',
    '177', '48',
    '87', '93',
    '117', '188',
    '90', '60',
    '104', '170',
    '54', '189',
]

def home(request):
    User = request.user
    Items = ItemsModel.objects.all()

    return render(request, 'tables/home.html', {'Items': Items, 'user': User})


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

def create_debt(date, user, total, joined = False):
    if joined:
        Debt.objects.create(
            customer = user,
            joined = True,
            debt = total,
            date = date,
        )
    else:
        Debt.objects.create(
            customer = user,
            single = True,
            debt = total,
            date = date
        )

@login_required
@csrf_exempt
def save_table_data(request):
    if request.method == 'POST':
        data = json.loads(request.body)['data']
        table_name = json.loads(request.body)['table_name']
        total = json.loads(request.body)['total-sum']
        date = json.loads(request.body)['date']
        joinedTables = User.objects.filter(is_supplier=True, username__in=["Կիրովական", "Արտադրամաս", "Փուռ"])
        items = ItemsModel.productsfor_Customer(request.user)

        if len(table_name) == 1:
            try:
                SingleTable.objects.get(
                    customer=request.user,
                    dateOfCreating=date
                )
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            except:
                pass
        else:
            try:
                JoinedTables.objects.get(
                    customer=request.user,
                    dateOfCreating=date
                )
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            except:
                pass



        if len(table_name) == 1:
            Create_old_debt(date=date, user=request.user)
        try:
            SingleTable.objects.get(dateOfCreating = date, customer = request.user)
        except:
            Create_old_debt(date=date, user=request.user)

        create_global_debt(date=date, user=request.user, total=total)

        if len(table_name) == 1:
            singleTabUsr = User.objects.filter(is_supplier=True).exclude(username__in=joinedTables.values('username')) 
            mainTable = SingleTable.objects.create(
                tableName = table_name,
                customer = request.user,
                dateOfCreating = date
                )
            for join, tabNam in zip(singleTabUsr, table_name):
                table = UserTable.objects.create(
                    user = request.user,
                    tableName = tabNam,
                    singleTable = mainTable,
                    dateOfCreating = date
                )
                for row in data:
                    if row['productCount'] == '':
                        row['productCount'] = 0
                    supTot = items.get(productName=row['productName']).supPrice * int(row['productCount']) 
                    table_item = TableItem.objects.create(
                        table=table,
                        product_name=row['productName'],
                        product_count=row["productCount"],
                        product_price=row['productPrice'],
                        total_price=row['totalPrice'],
                        customer = request.user,
                        supplier = join,
                        supTotal=supTot
                    )
                    table_item.save()

                    try:
                        big_tab = BigTableRows.objects.get(
                            user=request.user, 
                            supplier=join,
                            porduct_name=row['productName']
                            )
                        big_tab.item = table_item
                        big_tab.save()
                    except BigTableRows.DoesNotExist:
                        # Create a new BigTableRows object since it doesn't exist for the user and supplier.
                        big_tab = BigTableRows.objects.create(
                            user=request.user, 
                            supplier=join, 
                            item=table_item,
                            porduct_name=row['productName']
                            )
                        big_tab.save()

                try:
                    bigtable = BigTable.objects.get(supplier=join, user=request.user)
                    bigtable.table = table
                    bigtable.modifiedDate = date
                    bigtable.save()
                except BigTable.DoesNotExist:
                    bigtable = BigTable.objects.create(
                        supplier=join,
                        table=table,
                        user=request.user,
                        modifiedDate=date
                        )
            create_debt(date=date, user=request.user, total=total, joined = False)

            return JsonResponse({'message': 'Table data saved successfully'})
        
        mainTable = JoinedTables.objects.create(
            tableName = table_name, 
            customer = request.user,
            dateOfCreating = date
            )
        counter = 0
        for join, tabNam in zip(joinedTables, table_name):
            counter += 1
            if request.user.username in yerevan_schools and counter == 1:
                continue

            table = UserTable.objects.create(
                user = request.user,
                tableName = tabNam,
                joinedTable = mainTable,
                dateOfCreating = date
            )
            for row in data:
                if row['supplier'] == join.username:
                    if row['productCount'] == '':
                        row['productCount'] = 0
                    supTot = items.get(productName=row['productName']).supPrice * int(row['productCount'])
                    table_item = TableItem.objects.create(
                        table=table,
                        product_name=row['productName'],
                        product_count=row["productCount"],
                        product_price=row['productPrice'],
                        total_price=row['totalPrice'],
                        customer = request.user,
                        supplier = join,
                        supTotal=supTot
                    )
                    table_item.save()
      
                    try:
                        big_tab = BigTableRows.objects.get(
                            user=request.user, 
                            supplier=join,
                            porduct_name=row['productName']
                            )
                        big_tab.item = table_item
                        big_tab.save()
                    except BigTableRows.DoesNotExist:
                        # Create a new BigTableRows object since it doesn't exist for the user and supplier.
                        big_tab = BigTableRows.objects.create(
                            user=request.user, 
                            supplier=join, 
                            item=table_item,
                            porduct_name=row['productName']
                            )
                        big_tab.save()

            try:
                bigtable = BigTable.objects.get(supplier=join, user=request.user)
                bigtable.table = table
                bigtable.modifiedDate = date
                bigtable.save()
            except BigTable.DoesNotExist:
                bigtable = BigTable.objects.create(
                    supplier=join,
                    table=table,
                    user=request.user,
                    modifiedDate=date
                    )
                
        create_debt(date=date, user=request.user, total=total, joined=True)

        return JsonResponse({'message': 'Table data saved successfully'})
        # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    

def Paymant_View(request):
    if request.method == 'POST':
        form = PaymantForm(request.POST)
        if form.is_valid():
            debt = Paymant.objects.create(
                customer=request.user,
                money= int(request.POST.get('money')),
                returned = int(request.POST.get('returned')),
                salary = int(request.POST.get('salary')),
                date = request.POST.get('date')
                )
            latest_global_debt = Global_Debt.objects.filter(customer = request.user).latest('timeOfCreating')
            old_debt = Old_debt.objects.get(date=request.POST.get('date'), customer=request.user).debt
            # print(old_debt)
            debt_sum = latest_global_debt.debt - debt.money - debt.returned - debt.salary - old_debt
            weekDebt = Week_debt.objects.create(
                customer = request.user,
                date = request.POST.get('date'),
                debt = debt_sum
            )
            gloabalDebt = Global_Debt.objects.create(
                customer = request.user,
                debt = debt_sum + old_debt,
                date = request.POST.get('date')
            )

            # print(request.POST.get('date'), 'dateeee Payyy')
            debt.save()
            return redirect('tablesbyuser')
        return redirect('tablesbyuser')
    return redirect('tablesbyuser')

def sendOrder(request):
    if request.method == "POST": 
        data = json.loads(request.body)
        suplier_id = data['supplier_id']
        orderedTableName = data['nameOftable']
        customers = User.objects.filter(is_customer = True)
        supplier = User.objects.get(username = data['sup_name'])
        pTable = Ordered_Products_Table.objects.create(
            nameof_Table = orderedTableName,
            supplierof_Table = supplier,
        )
        pTable.save()

        for customer in customers:
            try:
                # print('Hello World!')
                custBigTable = BigTable.objects.get(
                    supplier_id = suplier_id,
                    user = customer
                    )
                columnof_Table = UserTable.objects.get(
                    tableName = custBigTable.table.tableName
                    )
                Ordered_Products_Column.objects.create(
                    parent_Table = pTable,
                    table = columnof_Table,
                    supplierof_table = supplier,
                ).save()
            except:
                continue
    
    return redirect('employee')
