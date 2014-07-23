//toggle element display
/*
function toggle(obj) {
	var element = document.getElementById(obj);

	if (element.style.display != 'none') {
		element.style.display = 'none';
	}
	else {
		element.style.display = '';
	}
}
*/
function toggleSlide(id) {
    
    if ($(id).css("display") == 'none') {
        $(id).slideDown("fast");
    }
    else {
        $(id).slideUp("fast");
    }
}

function toggleFadeAtScroll(id, scrollDist) {
    
    if ($.jStorage.get('scrollPosition') > scrollDist && $(id).css("display") == 'none') {
        $(id).fadeIn("slow");
    }
    if ($.jStorage.get('scrollPosition') < scrollDist) {
        $(id).fadeOut("slow");
    }
}
//keep fulltext searchbox checked???
	
function maintainSelect(id, jStoreVar, selectList) {
    if ($.jStorage.get(jStoreVar)) {
        var agencySel = $.jStorage.get(jStoreVar).join(", "); //get stored select-values from previous page filters
        $(id).val($.jStorage.get(jStoreVar)); //set the values for current page
        $(id).next().children('button').attr('title', agencySel); //set value="title" to select-value list
        $(id).next().children('button').children('.filter-option').text(agencySel); //set text to select-value list
        for (var i = 0; i < $.jStorage.get(jStoreVar).length; i++) { //activate each value manually (for tick marks -- purely aesthetic)
            var location = "li[rel='%s']".replace('%s', selectList[$.jStorage.get(jStoreVar)[i]]);
            $(id).next().children('.dropdown-menu').children('ul').children(location).attr('class', 'selected');
        }
    }
}

function deselect(id, noneSelText, selectList) {
	$(id).val('');
	$(id).next().children('button').attr('title', noneSelText);
    $(id).next().children('button').children('.filter-option').text(noneSelText);
	for (var i = 0; i < selectList.length; i++)
		$(id).next().children('.dropdown-menu').children('ul').children("li[rel='%s']".replace('%s', i)).attr('class', '');
}

function storeFilters() {
    $.jStorage.set('agencyVal', $('#agencies').val());
    $.jStorage.set('categoryVal', $('#categories').val());
    $.jStorage.set('typeVal', $('#types').val());
}

$(window).on('load', function () {
    $('.selectpicker').selectpicker({
        'selectedText': 'cat'
    });
	
    var agencies = {"Aging": 0, "Buildings": 1, "Campaign Finance": 2, "Children's Services": 3, "City Council": 4, "City Clerk": 5, "City Planning": 6, "Citywide Admin Svcs": 7, "Civilian Complaint": 8, "Comm - Police Corr": 9, "Community Assistance": 10, "Comptroller": 11, "Conflicts of Interest": 12, "Consumer Affairs": 13, "Contracts": 14, "Correction": 15, "Criminal Justice Coordinator": 16, "Cultural Affairs": 17, "DOI - Investigation": 18, "Design/Construction": 19, "Disabilities": 20, "District Atty, NY County": 21, "Districting Commission": 22, "Domestic Violence": 23, "Economic Development": 24, "Education, Dept. of": 25, "Elections, Board of": 26, "Emergency Mgmt.": 27, "Employment": 28, "Empowerment Zone": 29, "Environmental - DEP": 30, "Environmental - OEC": 31, "Environmental - ECB": 32, "Equal Employment": 33, "Film/Theatre": 34, "Finance": 35, "Fire": 36, "FISA": 37, "Health and Mental Hyg.": 38, "HealthStat": 39, "Homeless Services": 40, "Hospitals - HHC": 41, "Housing - HPD": 42, "Human Rights": 43, "Human Rsrcs - HRA": 44, "Immigrant Affairs": 45, "Independent Budget": 46, "Info. Tech. and Telecom.": 47, "Intergovernmental": 48, "International Affairs": 49, "Judiciary Committee": 50, "Juvenile Justice": 51, "Labor Relations": 52, "Landmarks": 53, "Law Department": 54, "Library - Brooklyn": 55, "Library - New York": 56, "Library - Queens": 57, "Loft Board": 58, "Management and Budget": 59, "Mayor": 60, "Metropolitan Transportation Authority": 61, "NYCERS": 62, "Operations": 63, "Parks and Recreation": 64, "Payroll Administration": 65, "Police": 66, "Police Pension Fund": 67, "Probation": 68, "Public Advocate": 69, "Public Health": 70, "Public Housing-NYCHA": 71, "Records": 72, "Rent Guidelines": 73, "Sanitation": 74, "School Construction": 75, "Small Business Svcs": 76, "Sports Commission": 77, "Standards and Appeal": 78, "Tax Appeals Tribunal": 79, "Tax Commission": 80, "Taxi and Limousine": 81, "Transportation": 82, "Trials and Hearings": 83, "Veterans - Military": 84, "Volunteer Center": 85, "Voter Assistance": 86, "Youth & Community": 87};
    var categories = {"Business and Consumers": 0, "Cultural/Entertainment": 1, "Education": 2, "Environment": 3, "Finance and Budget": 4, "Government Policy": 5, "Health": 6, "Housing and Buildings": 7, "Human Services": 8, "Labor Relations": 9, "Public Safety": 10, "Recreation/Parks": 11, "Sanitation": 12, "Technology": 13, "Transportation": 14};
    var types = {"Annual Report": 0, "Audit Report": 1, "Bond Offering - Official Statements": 2, "Budget Report": 3, "Consultant Report": 4, "Guide - Manual": 5, "Hearing - Minutes": 6, "Legislative Document": 7, "Memoranda - Directive": 8, "Press Release": 9, "Serial Publication": 10, "Staff Report": 11, "Report": 12};

    maintainSelect('#agencies', 'agencyVal', agencies);
    maintainSelect('#categories', 'categoryVal', categories);
    maintainSelect('#types', 'typeVal', types);
    
    $('.pagination').on('click', function() {
    	$.jStorage.set('scrollPosition',0);
    });
    //make sure paginate works appropriately to boostrap css standard
    $('.pagination').children('ul').attr('class', 'pagination')
});

$("#btn[value='Refine / Search']").click(storeFilters);

$("#btn[value='Search']").click(storeFilters);

$("#btn[value='Remove All']").on('click', function() {
	deselect('#agencies', 'All Agencies', agencies);
	deselect('#categories', 'All Categories', categories);
	deselect('#types', 'All Types', types);
});

//reset jStorage upon redirecting to home page
$("a[href='../index']").on('click', function() {
    $.jStorage.flush();
});

//make sure what is suppose to work works
$('.disabled').click(function(event){
    event.preventDefault();
});
$('.active').click(function(event){
    event.preventDefault();
});

//popover
$(function () {
    $('.popover-hover').popover( {
        trigger: 'hover',
        html: true,
        placement: 'right',
    });
});