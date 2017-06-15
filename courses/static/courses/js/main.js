$(document).ready(function(){
    $('#id_phone').mask('+0 (000) 000 00 00');
    $('#id_mobile_phone').mask('+0 (000) 000 00 00');
    $('#update-form').on('submit', function(event){
        event.preventDefault();
        var url = window.location.href.split('/');
        var data = $("#update-form").serializeArray();
        var form_json = Object();
        form_json.courses_list = [];
        for(i = 0; i < data.length ; i++){
            if(data[i].name == 'phone' || data[i].name == 'mobile_phone'){
                form_json[data[i].name] = data[i].value.replace(/[()\s]/g, '');
            }
            else if(data[i].name == 'courses_list'){
                form_json.courses_list.push(data[i].value);
            }
            else{
            form_json[data[i].name] = data[i].value;
        }
        }
        form_json = JSON.stringify(form_json);
        create_post(form_json);
    });
    $('#create-form').on('submit', function(event){
        event.preventDefault();
        var form_json = Object();
        var data = $("#create-form").serializeArray();
        for(i = 0; i < data.length ; i++){
            if(data[i].name == 'phone' || data[i].name == 'mobile_phone'){
                form_json[data[i].name] = data[i].value.replace(/[()\s]/g, '');
            }
            else{
                form_json[data[i].name] = data[i].value;
            }
        }
        form_json = JSON.stringify(form_json);
        create_post(form_json);
    });

})



function addCourse(){
    var course_select = document.getElementById('id_courses');
    var course_code = course_select.options[course_select.selectedIndex].value;
    var course_name = course_select.options[course_select.selectedIndex].text;
    course_select.options[course_select.selectedIndex].remove()
    var div = document.createElement('div')
    div.className = 'course'
    div.id = 'course-' + course_code
    var button = '<button id="button-' + course_code + '" class="remove-course" type="button"></button>';
    div.innerHTML = course_name + button;
    courses_list = document.getElementById('id_courses_list');
    courses_list = courses_list.getElementsByTagName('input');
    for(i = 0; i < courses_list.length; i++){
        if (courses_list[i].value == course_code){
            courses_list[i].checked = true;
            break;
        }
    }
    document.getElementsByClassName('course-container')[0].appendChild(div);
    document.getElementById('button-' + course_code).onclick = function(){
        removeCourse(course_name, course_code)
    }
    var amount = document.getElementsByClassName('course').length
    if (amount == 5) {
        divToHide  = course_select.parentElement
        divToHide.style.display = 'none'
    }

}
function removeCourse(name, code){
    var course_select = document.getElementById('id_courses');
    var amount = document.getElementsByClassName('course').length
    if (amount == 5) {
        divToHide  = course_select.parentElement
        divToHide.style.display = 'block'
    }
    document.getElementById('course-' + code).remove();
    var course = document.createElement("option");
    course.text = name;
    course.value = code;
    courses_list = document.getElementById('id_courses_list');
    courses_list = courses_list.getElementsByTagName('input');
    for(i = 0; i < courses_list.length; i++){
        if (courses_list[i].value == code){
            courses_list[i].checked = false;
            break;
        }
    }
    course_select.options.add(course);
}

function create_post(form_data) {
    $.ajax({
        url : "", // the endpoint
        type : "POST", // http method
        dataType: "json",
        data : {
            the_post : form_data,
            csrfmiddlewaretoken: csrf_token,
     }, // data sent with the post request

        // handle a successful response
        success : function(json) {
            $("div.success-div").remove();
            $("div.error").remove();
            inputs = $('input.error-symbol');
            if (inputs[0] != null){
                for(i=0; i<inputs.length; i++){
                    var errorClass = inputs[i].className;
                    inputs[i].className = errorClass.replace('error-symbol', '')
                }
            }
            if (typeof(json) == 'string'){
                json = JSON.parse(json);
            }
            if(json['type'] == 'error'){
                errs = json['err'];
                keys = Object.keys(errs);
                for(i=0; i < keys.length; i++){
                    var key = keys[i];
                    var input_id = '#id_' + key;
                    var error_html = errs[key][0];
                    var div = document.createElement('div');
                    div.className = 'error';
                    div.innerHTML = error_html;
                    var id = '#' + key;
                    var element = $(input_id)[0];
                    element.className = 'error-symbol'
                    element.style.color = '#FF2649';
                    $(input_id).keyup(function() {
                        element.style.color = 'black';
                    });
                    $(id)[0].appendChild(div);
                }
            }
            else{
                var url = window.location.origin;
                url = url + '/';
                var inscription = $("span.form-inscription")[0];
                inscription.marginTop = '0px';
                var div = document.createElement('div');
                div.className = 'success-div'
                if (json['type'] == 'update'){
                    div.innerHTML = '<b>Changes saved successfully</b>';
                }
                else{
                    div.innerHTML = '<b>User created successfully</b>';
                }
                var element = $('nav.navbar')[0]
                element.parentNode.insertBefore(div, element.nextSibling);
                if(json['type'] == 'create'){
                    window.setTimeout(function(){
                    window.location.href = url;
                    }, 3000);
                }
            }
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {s
        },
    });
};
