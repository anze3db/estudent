$('.dropdown-toggle').dropdown();

$(document).ready(function() {
	
	$('select[multiple=multiple]').attr('size', 20);
	$('select[multiple=multiple]#id_year').attr('size', 4);
	
	
    var last_valid_selection = null;

    $.fn.maxSelect = function(max){
    	$(this).change(function(event) {
            if ($(this).val().length > max) {
                alert('Izberete lahko maksimalno '+max+'!');
                $(this).val(last_valid_selection);
            } else {
                last_valid_selection = $(this).val();
            }
        });
    };
    $('#id_instructors').maxSelect(3);
    $('#id_modules').maxSelect(2);
    
    
    
    filter = function(element, getUrl, field){
    	/** 
    	 * Filters a select input by making a JSON request 
    	 * 	element - input selector
    	 * 	getUrl  - a function that returns an url to check
    	 * 	field   - field in returned data
    	 * 
    	 * */
    	var createHash = function(array){
    		// Create inverse hash for quicker lookup
        	var hash = {};
        	array.each(function(index, element){
        		if($(element).val() != "")
        			hash[$(element).val()] = index;
        	});
        	return hash;
        };
        this.filter = function(){
        	var filtered = [];
        	
        	$.getJSON(getUrl(), function(data){
        		for ( var i in data) {
    				filtered[filtered.length] = field(i, all, hash, data);
    			}
    			$(element).html(filtered);
        	});
        }
        var element = element;
    	var getUrl = getUrl;
    	var field = field;
    	var all  = $(element + " option");
    	var hash = createHash(all);
    };
    
    
    $.fn.busyChange = function(func){
    	/** Checks for a change ever 1/10s. Do not overuse! :D */
    	var element = this;
    	if($(element).length==0) return;
    	var tmp = this.val();
    	setInterval(function(){
    		if(tmp != element.val()){
    			tmp = element.val();
    			func();
    		}
    	}, 100);
    	
    };

    


    $("#id_birth_country").busyChange(function(){
    	if($("#id_birth_country").val() != "705"){
    		var social = $("#id_social_security_number");
    		if(social.val() && social.val().length > 7)
    			social.val(social.val().substring(0,7) + "000000");
    	}
    });
    if(document.URL.search(/codelist\/course/) < 0){
	    var instructorsFilter=new filter("#id_instructors", function(){
	        return '/api/getFilteredGroupInstructorsForCourses/?courseId='
	            +$("#id_course").val();
	    }, function(i, all, hash, data){
	    	return all[hash[data[i]["pk"]]];
	    });
	    instructorsFilter.filter();
	}
    $("#id_course").busyChange(function(){
        instructorsFilter.filter();
    });

    if(document.URL.search(/student\/examdate/) > 0){
    	var instructorsCFilter=new filter("#id_course", function(){
            return '/api/getFilterUserCourses/';
        }, function(i, all, hash, data){
        	return all[hash[data[i]["pk"]]];
        });
        instructorsCFilter.filter();    	
    	
    }
    else if(document.URL.search(/student\/curriculum/) < 0){
        var courseProgramFilter=new filter("#id_course", function(){
            return '/api/getFilteredCourses/?programId='
                +$("#id_prog").val();
        }, function(i, all, hash, data){
        	return all[hash[data[i]['fields']['course']]];
        });
        courseProgramFilter.filter();

        $("#id_prog").busyChange(function(){
        	courseProgramFilter.filter();
        });
        
        // Filter courses:
        var courseFilter = new filter("#id_courses", function(){
        	var url = document.URL.split('/');
        	var id  = url[url.length-2];
        	var modules = ($("#id_modules").val() instanceof Array) ? $("#id_modules").val().join(',') : $("#id_modules").val();
        	return '/api/getFilteredCoursesModules/?program='
        	+$("#id_program").val()+'&year='
        	+$("#id_class_year").val()+'&modules='
        	+modules+'&student='
        	+$("#id_student").val()+'&id='
        	+id+'&vrsta='+$("#id_enrol_type").val();
        }, function(i, all, hash, data){
        	 return all[hash[data[i].fields["course"]]];
        });
        courseFilter.filter();
        $("#id_student").busyChange(function(){
        	courseFilter.filter();
        });
    }
    var moduleFilter = new filter("#id_modules", function(){
    	return '/api/getFilteredModules/?program='
    	+$("#id_program").val()+'&year='
    	+$("#id_class_year").val();
    }, function(i, all, hash, data){
    	return all[hash[data[i]["pk"]]];
    });
    moduleFilter.filter();
    $("#id_enrol_type").busyChange(function(){
    	courseFilter.filter();
    });
    $("#id_class_year").busyChange(function(){
    	courseFilter.filter();
    	moduleFilter.filter();
    });
    $("#id_program").busyChange(function(){
    	courseFilter.filter();
    	moduleFilter.filter();
    });
    $("#id_modules").change(function(){
    	courseFilter.filter();
    });
    
    
    
});



