let sale = {
    leds: []
};

function isValidEmailAddress(emailAddress) {
    let pattern = /^([a-z\d!#$%&'*+\-\/=?^_`{|}~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]+(\.[a-z\d!#$%&'*+\-\/=?^_`{|}~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]+)*|"((([ \t]*\r\n)?[ \t]+)?([\x01-\x08\x0b\x0c\x0e-\x1f\x7f\x21\x23-\x5b\x5d-\x7e\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]|\\[\x01-\x09\x0b\x0c\x0d-\x7f\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]))*(([ \t]*\r\n)?[ \t]+)?")@(([a-z\d\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]|[a-z\d\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF][a-z\d\-._~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]*[a-z\d\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])\.)+([a-z\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]|[a-z\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF][a-z\d\-._~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]*[a-z\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])\.?$/i;
    return pattern.test(emailAddress);
}

function updateSale(sale_data) {
    $.ajaxSetup({
        headers: {
            "X-CSRFToken": $("input[name='csrfmiddlewaretoken']").val()
        }
    });
    $.ajax({
        type: "POST",
        url: "/sale/update/",
        data: JSON.stringify(sale_data), 
        success: function(data){
            return data;
        },
        fail: function(data){
            alert('unknown error occurred');
        }
    });
}

// drag and drop: remove LED
function allowDrop(event) {
    event.preventDefault();
}


// drag and drop: remove LED
function trashLED(event) {
    event.preventDefault();
    let led_id = event.dataTransfer.getData("led_id");
    console.log(sale);
    for(let i = 0; i < sale.leds.length; i++){
        if( sale.leds[i].id == led_id ){
            sale.leds.splice(i, 1);
            $(`#${led_id}`).hide();
        }
    }
}

// drag and drop: remove LED
function toggleTrash(event){
    event.dataTransfer.setData("led_id", event.target.id);
    $('.led-header, .led-trash').toggle();
}

$(document).on('change', ':file', function() {
    var input = $(this),
        numFiles = input.get(0).files ? input.get(0).files.length : 1,
        label = input.val().replace(/\\/g, '/').replace(/.*\//, '');
    input.trigger('fileselect', [numFiles, label]);
});

$(document).ready(function(){
    $.ajaxSetup({
        headers: {
            "X-CSRFToken": $("input[name='csrfmiddlewaretoken']").val()
        }
    });

    //signin/register indentifiers
    $("login, register").on('click',function() {
        //remove active identfier
        $("login, register").removeClass('login-active');

        //Add active class to clicked element
        $(this).addClass('login-active');

        //toggle shown forms
        $("#login-card, #register-card").toggle();
    });


    //Register form
    $("form[name='register-form']").submit(function(event) {
        //Stop html form submission
        event.preventDefault(); 

        //validate
        let form_inputs = [
            $("input[name='register-username']"),
            $("input[name='register-email']"),
            $("input[name='register-password']"),
            $("input[name='register-confirm-password']"),
            $("input[name='register-company']"),
        ];
        
        //check for blanks
        for ( i in form_inputs ) { 
            if( !form_inputs[i].val() ){
                //add border
                form_inputs[i].css('border','1px solid red').focus();
                //reset input 
                setTimeout(function resetInput() {
                    form_inputs[i].css("border","0px");
                }, 3000);
                return;
            }
        }

        //check email validatity
        if( !isValidEmailAddress(form_inputs[2].val()) ){
            //add border
            form_inputs[2].css('border','1px solid red').focus();
            //reset input 
            setTimeout(function resetInput() {
                form_inputs[2].css("border","0px");
            }, 3000);

        }

        //confirm password
        if( form_inputs[2].val() !== form_inputs[3].val() ){
            //add border
            form_inputs[2].css('border','1px solid red').focus();
            form_inputs[3].css('border','1px solid red');
            //reset input 
            setTimeout(function resetInput() {
                form_inputs[2].css("border","0px");
                form_inputs[3].css("border","0px");
            }, 3000);
            return;
        }else{
            // serialize and submit register form
            $.ajax({
                type: "POST",
                url: $(this).attr('action'),
                data: $(this).serialize(), 
                success: function(data){
                    if( data.status == 'success'){
                        window.location.href = window.location.protocol + "//" + window.location.host + "/dashboard/";
                    }else{
                        $('#login-header, #login-error').toggle();
                        $('.error-msg').text(data.error_msg);
                        setTimeout(function resetInput() {
                            $('#login-header, #login-error').toggle();
                        }, 3000);

                    }
                },
                fail: function(data){
                    alert('unknown error occurred');
                }
            });
        }
    });


    //login form
    $("form[name='login-form']").submit(function(event) {
        //Stop html form submission
        event.preventDefault(); 

        //validate
        let username = $("input[name='username']").val();
        let password = $("input[name='password']").val();
        
        //check for blanks
        if( !username || !password ){
            //add border
            $("input[name='username'], input[name='password']").css('border','1px solid red');
            //reset input 
            setTimeout(function resetInput() {
                $("input[name='username'], input[name='password']").css("border","0px");
            }, 3000);
            return;

        }else{
            // serialize and submit login form
            $.ajax({
                type: "POST",
                url: $(this).attr('action'),
                data: $(this).serialize(), 
                success: function(data){
                    if( data.status == 'success'){
                        //redirect to homepage
                        window.location.href = window.location.protocol + "//" + window.location.host + "/dashboard/";
                    }else{
                        $('#login-header, #login-error').toggle();
                        $('.error-msg').text(data.error_msg);
                        setTimeout(function resetInput() {
                            $('#login-header, #login-error').toggle();
                        }, 3000);
                    }
                },
                fail: function(data){
                    alert('unknown error occurred');
                }
            });
        }
    });


    // renewal
    $(".renewal-option").on('click',function() {
        $(".renewal-option").removeClass('renewal-option-selected');

        //Add active class to clicked element
        $(this).addClass('renewal-option-selected');

        // set sale value
        if( $(this).attr('data-type') == 'renewal' ){
            sale.renewal = true;
        }else{
            sale.renewal = false;
        }
    });


    // subtype/HOO autofill
    $("#subtype-dropdown").on('change',function() {
        // get HOO info from dropdown
        let subtype = $("#subtype-dropdown option:selected").val();
        
        if( !subtype ){
            sale.subtype = null;
            return;
        }else{
            sale.subtype = subtype;
        }

        let hours_of_operation = JSON.parse($("#subtype-dropdown option:selected").attr('data'));
        //  auto fill values
        $("input[name='monday']").val(hours_of_operation.monday);
        $("input[name='tuesday']").val(hours_of_operation.tuesday);
        $("input[name='wednesday']").val(hours_of_operation.wednesday);
        $("input[name='thursday']").val(hours_of_operation.thursday);
        $("input[name='friday']").val(hours_of_operation.friday);
        $("input[name='saturday']").val(hours_of_operation.saturday);
        $("input[name='sunday']").val(hours_of_operation.sunday);
        $("input[name='total']").val(hours_of_operation.total);
    });


    // autocalculate HOO
    $(".weekly-hours").keyup(function() {
        let current_input_value = $(this);
        let all_other_hours = 0;
        
        // get all other hours
        $(".weekly-hours").not(current_input_value).each(function(){
            all_other_hours += Number($(this).val());
        });

        // get weekly total and multiple for the yearly
        new_total = (Number(current_input_value.val()) + all_other_hours) * 52.143;
        $("input[name='total']").val(Math.trunc(new_total));
    });


    // New Sale: customer info
    $("form[name='new-sale-customer-info']").submit(function(event){
        //Stop html form submission
        event.preventDefault();

        // check renewal/subtype selected
        if( !sale.renewal ){
            $(".renewal-option").attr("tabindex",-1).focus().css("border-color", "red");
            setTimeout(function(){
                $(".renewal-option").css("border-color", "");
            },2000);
        }

        // check for blanks
        let require_fields = [
            $("input[name='business-name']"),
            $("input[name='auth-rep']"),
            $("input[name='service-address']"),
            $("input[name='service-city']"),
            $("input[name='service-state']"),
            $("input[name='service-zip-code']"),
            $("input[name='total']")
        ]; 

        for( field in require_fields ){
            if( !$(field).val() ){
                $(field).focus();
            }
        }

        // update sale obj
        sale.business_name = require_fields[0].val();
        sale.auth_rep = require_fields[1].val();
        sale.service_address = require_fields[2].val();
        sale.service_city = require_fields[3].val();
        sale.service_state = require_fields[4].val();
        sale.service_zip_code = require_fields[5].val();
        sale.annual_hours_of_operation = require_fields[6].val();

        // UpdateSale
        updateSale(sale);

        // toggle cards
        $("#customer-info-card, #led-selection-card").toggle();
    });


    // led selection back
    $(".led-selection-back").click(function(e){
        // stop form submission
        event.preventDefault();
        // toggle cards
        $("#led-selection-card").hide();
        $("#customer-info-card").show();
    });


    // sales table
    $('#sales-table').DataTable();


    // show led counting  
    $('.led-option').click(function(e){
        let led_id = $(this).attr('data-id');
        $('.led-counts').slideUp();
        $(`.led-counts[data-id=${led_id}]`).slideToggle();
    });


    // led counting
    $("input[name='led-count'], input[name='led-total'], input[name='led-delamping']").keyup(function(e){
        let led_id = $(this).attr('data-id');
        let total = Number($(`input[name='led-total'][data-id=${led_id}]`).val());
        let led_count = Number($(`input[name='led-count'][data-id=${led_id}]`).val());
        let delamping = Number($(`input[name='led-delamping'][data-id=${led_id}]`).val());
        $(`input[name='led-not-replacing'][data-id=${led_id}]`).val(total - (led_count + delamping));    
    });


    // add led to sale
    $("form[name='led-to-sale-form']").submit(function(event) {
        //Stop html form submission
        event.preventDefault(); 

        // gen LED obj
        let led_id = Number($(this).attr('data-id'));
        let total = Number($(`input[name='led-total'][data-id=${led_id}]`).val());
        let led_count = Number($(`input[name='led-count'][data-id=${led_id}]`).val());
        let delamping = Number($(`input[name='led-delamping'][data-id=${led_id}]`).val());
        let not_replacing = Number($(`input[name='led-not-replacing'][data-id=${led_id}]`).val()); 
        let color = $(`.led-color[data-id=${led_id}] option:selected`).val();
        let installation = $(this).find(".active").attr('data-type');
        let ceiling_height = $(`.ceiling-height-dropdown[data-id=${led_id}] option:selected`).val();
        let led = {
            id: Math.floor((Math.random() * 100) + 1),
            led_id: led_id,
            total_lights: total,
            led_count: led_count,
            delamping: delamping,
            not_replacing: not_replacing,
            color: color,
            installation: installation,
            ceiling_height: ceiling_height
        };
        // add led to sale
        sale.leds.push(led);
        
        // clone element into selected
        $(`.led-counts[data-id=${led_id}]`).slideUp();
        $(`.led-option[data-id=${led_id}]`).clone().addClass('led-on-sale').prop({'id': led.id, "draggable": true}).appendTo('#selected-leds');
    });


    // LED selection: next
    $("form[name='new-sale-leds']").submit(function(e) {
        //Stop html form submission
        e.preventDefault(); 

        console.log(sale);
        if( sale.leds.length > 0 ){
            updateSale(sale);
        }

        // toggle cards
        $("#led-selection-card, #bill-info-card").toggle();
    });


    // Bill info back
    $(".bill-info-back").click(function(e){
        $("#led-selection-card, #bill-info-card").toggle();
    });


    // service billing same
    $("#billing-service-address-same").click(function(e){
        if( $(this).prop('checked') ){
            $("#billing-address").slideUp("fold");
            $("input[name='billing-address']," +
              "input[name='billing-city']," + 
              "input[name='billing-state']," + 
              " input[name='billing-state']," + 
              " billing-zip-code").prop('required', false);
        }else {
            $("#billing-address").slideDown("fold");
            $("input[name='billing-address']," +
              "input[name='billing-city']," + 
              "input[name='billing-state']," + 
              " input[name='billing-state']," + 
              " billing-zip-code").prop('required', true);
        }
    });


    // utility dropdown
    $("#utility-dropdown").change(function(e){
        let utility = $("#utility-dropdown option:selected");
        let account_length = JSON.parse(utility.attr('data')).account_length

        // add utility to sale obj
        sale.utility = utility.val();

        // add account limit length to account input
        $("input[name='account-number'").attr({maxlength:account_length, minlength: account_length});
    });


    // monthly/yearly usage
    $(".usage-option").click(function(){
        // show selected
        $(".usage-option").removeClass("usage-option-selected");
        $(this).addClass("usage-option-selected");

        // change require fields
        if( $(this).attr("data-type") == 'monthly' ){
            $("#yearly-usage").hide("fold");
            $("#monthly-usage").slideDown();
            $("input[name='monthly-kwh'], input[name='monthly-supply-charges'],input[name='monthly-delivery-charges']").prop('required', true);
            $("input[name='yearly-kwh'], input[name='yearly-supply-charges'],input[name='yearly-delivery-charges']").prop('required', false);
        }else {
            $("#monthly-usage").hide("fold");
            $("#yearly-usage").slideDown();
            $("input[name='yearly-kwh'], input[name='yearly-supply-charges'],input[name='yearly-delivery-charges']").prop('required', true);
            $("input[name='monthly-kwh'], input[name='monthly-supply-charges'],input[name='monthly-delivery-charges']").prop('required', false);
        }
    });


    // bill image
    $(':file').on('fileselect', function(event, numFiles, label) {
        console.log(numFiles);
        console.log(label);
    });


    // service satrt date
    $("input[name='service-start-date']").datepicker();


    // bill info form
    $("form[name='bill-info-form']").submit(function(e){
        //Stop html form submission
        e.preventDefault(); 

        
        // handle billing address
        if( $("#billing-service-address-same").prop('checked') ){
            sale.billing_address = sale.service_address;
            sale.billing_city = sale.service_city;
            sale.billing_state = sale.service_state;
            sale.billing_zip_code = sale.service_zip_code;
        }else{
            sale.billing_address = $("input[name='billing-address']");
            sale.billing_city = $("input[name='billing-city']");
            sale.billing_state = $("input[name='billing-state']");
            sale.billing_zip_code = $("input[name='billing-zip-code']");
        }
        
        sale.utility = $("#utility-dropdown option:selected").val();
        sale.service_class = $("#service-class-dropdown option:selected").val();
        sale.account_number = $("input[name='account-number']").val();

        let bill_type = $(".usage-option-selected").attr('data-type');
        let bill = {};
        
        if( bill_type === 'monthly'){
            bill.type = bill_type;
            bill.kwh = $("input[name='monthly-kwh']");
            bill.supply_charges = $("input[name='monthly-supply-charges']");
            bill.delivery_charges = $("input[name='monthly-delivery-charges']");
        }else if( bill_type === 'yearly'){
            bill.type = bill_type;
            bill.kwh = $("input[name='yearly-kwh']");
            bill.supply_rate = $("input[name='supply-rate']");
        }else{
            alert('Please choose a usage type monthly/yearly.');
        }
        bill.month = $("#month-of-bill-dropdown option:selected").val();

        let bill_image = document.getElementById('bill-image').files[0]
        if( bill_image ){
            bill.image = bill_image;
        }

        sale.bill = bill;

        sale.service_start_date = $("input[name='service-start-date']").val();

        console.log(sale);
    });
});