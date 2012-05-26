$('.dropdown-toggle').dropdown();

$(document).ready(function() {
    var last_valid_selection = null;

    $('#id_instructors').change(function(event) {
        if ($(this).val().length > 3) {
            alert('Izberete lahko maksimalno 3 predavatelje!');
            $(this).val(last_valid_selection);
        } else {
            last_valid_selection = $(this).val();
        }
    });
    
    
    var filter = function(element, getUrl, field){
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
        		hash[$(element).val()] = index;
        	});
        	return hash;
        };
        this.filter = function(){
        	var filtered = [];
        	$.getJSON(getUrl(), function(data){
        		for ( var i in data) {
    				filtered[filtered.length] = all[hash[data[i].fields[field]]];
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
    
    // Filter courses:
    var courseFilter = new filter("#id_courses", function(){
		return '/api/getFilteredCoursesModules/?program='
					   +$("#id_program").val()+'&year='
					   +$("#id_class_year").val();
    }, "course");
    courseFilter.filter();
    
    $.fn.busyChange = function(func){
    	/** Checks for a change ever 1/10s. Do not overuse! :D */
    	
    	var element = this;
    	var tmp = this.val();
    	setInterval(function(){
    		if(tmp != element.val()){
    			tmp = element.val();
    			func();
    		}
    	}, 100);
    	
    };

	$("#id_class_year").busyChange(function(){
		courseFilter.filter();
	});
	$("#id_program").busyChange(function(){
		courseFilter.filter();
	});

    var instructorsFilter=new filter("#id_groupinstructors", function(){
        return '/api/getFilteredGroupInstructorsForCourses/?courseId='
            +$("#id_course").val();
    }, "instructors");
    instructorsFilter.filter();


    $("#id_course").busyChange(function(){
        instructorsFilter.filter();
    });

});



