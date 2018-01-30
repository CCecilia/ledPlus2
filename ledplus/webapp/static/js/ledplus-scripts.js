function isValidEmailAddress(emailAddress) {
    let pattern = /^([a-z\d!#$%&'*+\-\/=?^_`{|}~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]+(\.[a-z\d!#$%&'*+\-\/=?^_`{|}~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]+)*|"((([ \t]*\r\n)?[ \t]+)?([\x01-\x08\x0b\x0c\x0e-\x1f\x7f\x21\x23-\x5b\x5d-\x7e\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]|\\[\x01-\x09\x0b\x0c\x0d-\x7f\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]))*(([ \t]*\r\n)?[ \t]+)?")@(([a-z\d\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]|[a-z\d\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF][a-z\d\-._~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]*[a-z\d\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])\.)+([a-z\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]|[a-z\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF][a-z\d\-._~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]*[a-z\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])\.?$/i;
    return pattern.test(emailAddress);
}

function updateSale(sale) {
    $.ajax({
        type: "POST",
        url: "/updateSale/",
        data: JSON.stringify(sale), 
        success: function(data){
            if( data.status == 'success'){
                return data
            }else{
                return data
            }
        },
        fail: function(data){
            alert('unknown error occurred');
        }
    });
}


$(document).ready(function(){
    let sale = {};

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
                        console.log('success');
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


    // new sale
    // renewal
    $(".renewal-option").on('click',function() {
        console.log('renewal');
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
            $("input[name='total']"),
        ]; 

        for( field in require_fields ){
            if( !$(field).val() ){
                $(field).focus();
            }else if( $(field).attr('name') === 'service-zip-code' && $(field).val().length != 5 ){
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
        sale.hoo_total = require_fields[6].val();

        // UpdateSale and show next section of form
        let update = updateSale(sale);
        
        if( update.status === 'success' ){
            console.log('success');
            sale.id = data.sale_id;
        }else{
            console.log(update.error);
            alert(update.error_msg);
        }

    });
});