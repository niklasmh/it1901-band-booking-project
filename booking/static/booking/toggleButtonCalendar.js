	const toggleID = document.getElementById("toggleCalendar")
	const weekview = document.getElementById("weekcalendar")
	const calendarview = document.getElementById("monthCalendar")
	calendarview.style.display = "none";

    toggleID.innerHTML = '<button class="button" id="toggleButton" onclick="togglecalendar()">' +  "Calendar view" + '</button>'

    var toggleButton = document.getElementById("toggleButton")
	function togglecalendar(){
		if (weekview.style.display != "none"){
			weekview.style.display = "none";
			calendarview.style.display = "block"
			toggleID.innerHTML = '<button class="button" id="toggleButton" onclick="togglecalendar()">' +  "Week view" + '</button>'
		} else if (weekview.style.display === "none") {
			weekview.style.display = "block";
			calendarview.style.display = "none"
			toggleID.innerHTML = '<button class="button" id="toggleButton" onclick="togglecalendar()">' +  "Calendar view" + '</button>'
		}
	}