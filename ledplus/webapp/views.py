__author__ = 'christian.cecilia1@gmail.com'
import csv
from dateutil.parser import parse as dateParse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
import json
from .models import *


class HtmlRendering:

	def index(request):
		context = {
			'page': 'index',
		}
		return render(request, 'webapp/index.html', context)

	@login_required
	def dashboard(request):
		user = request.user
		if request.user.is_staff:
			sale_count = Sale.objects.all().count()
		else:
			sale_count = Sale.objects.filter(agent=request.user).count()

		context = {
			'page': 'dashboard',
			'user': user,
			'sale_count': sale_count
		}
		return render(request, 'webapp/dashboard.html', context)

	@login_required
	def newSale(request):
		user = request.user
		
		context = {
			'page': 'new sale',
			'subtypes': Subtype.objects.all().order_by('name'),
			'leds': Led.objects.filter(active=True).order_by('order_number'),
			'utilities': Utility.objects.filter(active=True).order_by('name'),
			'service_classes': ServiceClass.objects.filter(active=True).order_by('name'),
		}
		return render(request, 'webapp/new-sale.html', context)

	@login_required
	def sales(request):
		if request.user.is_staff:
			sales = Sale.objects.all()
		else:
			sales = Sale.objects.filter(agent=request.user)

		context = {
			'page': 'sales',
			'sales': sales
		}
		return render(request, 'webapp/sales.html', context)

	@login_required
	def saleSavings(request, sale_id):
		sale = get_object_or_404(Sale, pk=sale_id)
		SaleViews.calculateSavings(sale)

		context = {
			'page': 'Savings',
			'sale': sale
		}
		return render(request, 'webapp/saleSavings.html', context)


class UserViews:

	def register(request):
		# dec vars
		username = str(request.POST['register-username']).lower()
		company = str(request.POST['register-company']).upper()
		email = str(request.POST['register-email']).lower()
		password = str(request.POST['register-password'])

		# check if username or email is used
		username_check = User.objects.filter(username=username)
		email_check = User.objects.filter(email=email)

		if username_check:
			response = {
				'status': 'fail',
				'error_msg': 'username already in use'
			}
			# send reponse JSON
			return JsonResponse(response)
		elif email_check:
			response = {
				'status': 'fail',
				'error_msg': 'email already in use'
			}
			# send reponse JSON
			return JsonResponse(response)
		elif len(password) < 8:
			response = {
				'status': 'fail',
				'error_msg': 'password must be atleast 8 characters long'
			}
			# send reponse JSON
			return JsonResponse(response)
		else:
			# create user
			user = User.objects.create_user(username, email, password)
			# create abstract agent model
			Agent.objects.create(user=user, company=company)

			# login user
			login(request, user)

			response = {
				'status': 'success'
			}
		# send reponse JSON
		return JsonResponse(response)

	def login(request):
		# dec vars
		username = request.POST['username']
		password = request.POST['password']

		# Auth user
		user = authenticate(request, username=username, password=password)

		if not user:
			# create response
			response = {
				'status': 'fail',
				'error_msg': 'username/password incorrect'
			}
		else:
			# login user
			login(request, user)

			response = {
				'status': 'success'
			}

		# send reponse JSON
		return JsonResponse(response)

	def logout(request):
		# log out user
		logout(request)

		# send to home page
		return redirect('/')


class SaleViews:

	def addLEDs(sale, leds):
		# clear any existing leds
		[sale.leds.remove(led) for led in sale.leds.all()]

		# create SaleLed obj and associate to sale
		for i in range(len(leds)):
			led = Led.objects.get(id=leds[i]['led_id'])

			# calc wattage reduction
			hoo = int(sale.annual_hours_of_operation)
			wattage_difference = float(led.conventional_wattage) - float(led.wattage)
			# delamp_wattage = leds[i].delamping * float(led.conventional_wattage)
			led_wattage_reduction = wattage_difference * leds[i]['led_count']
			delamp_wattage_reduction = float(led.conventional_wattage) * leds[i]['delamping']
			total_wattage_reduction = led_wattage_reduction + delamp_wattage_reduction
			total_kWh_reduction = (total_wattage_reduction * hoo) / 1000
			
			# js true to python True
			if leds[i]['installation'] == 'true':
				leds[i]['installation'] = True
			else:
				leds[i]['installation'] = False

			sale_led = SaleLed.objects.create(
				led=led,
				color=leds[i]['color'],
				led_count=leds[i]['led_count'],
				total_count=leds[i]['total_lights'],
				not_replacing_count=leds[i]['not_replacing'],
				delamping_count=leds[i]['delamping'],
				wattage_reduction=total_kWh_reduction,
				installation_required=leds[i]['installation'],
				ceiling_height=leds[i]['ceiling_height']
			)
			sale.leds.add(sale_led)

	def uploadBillImage(request):
		bill_image = request.FILES['bill_image']
		sale_id = request.POST['sale_id']
		sale = get_object_or_404(Sale, pk=sale_id)
		sale.bill_image = bill_image

		try:
			sale.save()
			response = {
				'status': 200
			}
		except Exception as e:
			response = {
				'status': 500,
				'error_msg': str(e)
			}
		return HttpResponse(response)

	def update(request):
		# dec vars
		sale_data = json.loads(request.body)

		# check create or update existing
		try:
			sale_id = sale_data['id']
			sale = get_object_or_404(Sale, pk=sale_id)
		except KeyError:
			sale = Sale.objects.create(
				agent=request.user
			)

		# handle customer info
		if sale_data['customer_info']:
			sale.renewal = sale_data['customer_info']['renewal']
			sale.business_name = sale_data['customer_info']['business_name']
			sale.authorized_representative = sale_data['customer_info']['auth_rep']
			sale.service_address = sale_data['customer_info']['service_address']
			sale.service_city = sale_data['customer_info']['service_city']
			sale.service_state = sale_data['customer_info']['service_state']
			sale.service_zip_code = sale_data['customer_info']['service_zip_code']
			subtype = Subtype.objects.get(id=sale_data['customer_info']['subtype'])
			sale.subtype = subtype
			sale.annual_hours_of_operation = sale_data['customer_info']['annual_hours_of_operation']

		# handle leds
		if len(sale_data['leds']) > 0:
			leds = sale_data['leds']
			SaleViews.addLEDs(sale, leds)
		elif len(sale_data['leds']) == 0:
			[sale.leds.remove(led) for led in sale.leds.all()]

		# handle bill info
		if sale_data['bill_info']:
			sale.billing_address = sale_data['bill_info']['billing_address']
			sale.billing_city = sale_data['bill_info']['billing_city']
			sale.billing_state = sale_data['bill_info']['billing_state']
			sale.billing_zip_code = sale_data['bill_info']['billing_zip_code']
			sale.utility = Utility.objects.get(id=sale_data['bill_info']['utility'])
			
			# add zone to sale if needed
			if sale.utility.zone_lookup:
				zone_match = [zone for zone in  sale.utility.zones.all() if zone.zip_code == sale.service_zip_code[:5]]
				if zone_match:
					sale.zone = zone_match[0]
				else:
					response = {
						'status': 'fail',
						'error_msg': 'Utility uses zones but customer\'s zone not found in system'
					}
					# send reponse JSON
					return JsonResponse(response)
			
			sale.service_class = ServiceClass.objects.get(id=sale_data['bill_info']['service_class'])
			
			if Sale.objects.filter(utility_account_number=sale_data['bill_info']['account_number']).exclude(id=sale.id):
				response = {
					'status': 'fail',
					'error_msg': 'Account number is already in use.'
				}
				# send reponse JSON
				return JsonResponse(response)

			sale.utility_account_number = sale_data['bill_info']['account_number']
			sale.bill_type = sale_data['bill_info']['bill_type']
			sale.month_of_bill = sale_data['bill_info']['month_of_bill']

			# check bill type
			if sale_data['bill_info']['bill_type'] == 'monthly':
				sale.supply_charges = sale_data['bill_info']['supply_charges']
				sale.delivery_charges = sale_data['bill_info']['delivery_charges']
				# estimate annual kwh
				estimated_annual_kwh = int(sale_data['bill_info']['kwh']) / 0.0804
				sale.kwh = estimated_annual_kwh
			else:
				sale.supply_rate = sale_data['bill_info']['supply_rate']
				sale.kwh = sale_data['bill_info']['kwh']

			# ensure service start date is in future
			today = timezone.now()
			if dateParse(sale_data['bill_info']['service_start_date']).date() <= today.date():
				response = {
					'status': 'fail',
					'error_msg': 'Service start date must be in the future.'
				}
				# send reponse JSON
				return JsonResponse(response)

			sale.service_start_date = dateParse(sale_data['bill_info']['service_start_date']).date()

		try:
			sale.save()
			response = {
				'status': 'success',
				'sale_id': sale.id
			}
		except Exception as e:
			response = {
				'status': 'fail',
				'error_msg': str(e)
			}

		# send reponse JSON
		return JsonResponse(response)

	def calculateSavings(sale):
		# check sale has rate
		if not sale.base_rate:
			RateViews.findRate(sale)
		return


class RateViews:

	def findRate(sale):
		# get rate sheet
		rate_sheet = sale.agent.agent.retail_energy_provider.rate_upload
		# open
		with open(rate_sheet.path) as ratesfile:
			reader = list(csv.reader(ratesfile))
			# get headers/gen col keys
			headers = dict([(str(reader[0][i]).lower().replace(' ','_'), i) for i in range(len(reader[0]))])
			# start filter down for rate
			state_rates = [row for row in reader if row[headers['state']] == sale.service_state]
			if len(state_rates) == 0:
				return {'status': 'failed', 'error_msg': 'failed on state'}
			
			utility_rates = [row for row in state_rates if str(row[headers['utility']]).upper() == str(sale.utility.name).upper()]
			if len(utility_rates) == 0:
				return {'status': 'failed', 'error_msg': 'failed on utility'}


			print('init: {}, state: {}, utility: {}'.format(len(reader), len(state_rates), len(utility_rates)))
			

		return
