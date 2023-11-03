
document.addEventListener("DOMContentLoaded", function () {
    const calendarBody = document.getElementById("calendar-body");
    const currentMonthYear = document.getElementById("current-month-year");
    const selectedDate = document.getElementById("selected-date");
    const taskList = document.getElementById("task-list"); // Update the task list

    const months = [
        "January", "February", "March", "April",
        "May", "June", "July", "August",
        "September", "October", "November", "December"
    ];

    const daysOfWeek = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

    let currentDate = new Date();
    let currentMonth = currentDate.getMonth();
    let currentYear = currentDate.getFullYear();

    // Function to generate the calendar
    function generateCalendar() {
        currentMonthYear.textContent = months[currentMonth] + " " + currentYear;

        // Clear the calendar body
        calendarBody.innerHTML = "";

        const firstDay = new Date(currentYear, currentMonth, 1);
        const lastDay = new Date(currentYear, currentMonth + 1, 0);

        // Create rows for each week
        let date = new Date(firstDay);
        while (date <= lastDay) {
            const weekRow = document.createElement("tr");
            for (let i = 0; i < 7; i++) {
                const cell = document.createElement("td");
                if (date >= firstDay && date <= lastDay) {
                    cell.textContent = date.getDate();
                    cell.addEventListener("click", () => displayTasks(new Date(date)));
                    if (date.toDateString() === currentDate.toDateString()) {
                        cell.classList.add("current-date");
                    }
                }
                weekRow.appendChild(cell);
                date.setDate(date.getDate() + 1);
            }
            calendarBody.appendChild(weekRow);
        }
    }

    // Add event listeners for previous and next month buttons
    document.getElementById("prev-month").addEventListener("click", function () {
        currentMonth--;
        if (currentMonth < 0) {
            currentMonth = 11;
            currentYear--;
        }
        generateCalendar();
        displayTasks(currentDate); // Display tasks for the current date
    });

    document.getElementById("next-month").addEventListener("click", function () {
        currentMonth++;
        if (currentMonth > 11) {
            currentMonth = 0;
            currentYear++;
        }
        generateCalendar();
        displayTasks(currentDate); // Display tasks for the current date
    });

    while (date <= lastDay) {
        const weekRow = document.createElement("tr");
        for (let i = 0; i < 7; i++) {
            const cell = document.createElement("td");
            if (date >= firstDay && date <= lastDay) {
                cell.textContent = date.getDate();
                cell.addEventListener("click", () => displayTasks(new Date(date)));
                if (date.toDateString() === currentDate.toDateString()) {
                    cell.classList.add("current-date");
                }
            }
            weekRow.appendChild(cell);
            date.setDate(date.getDate() + 1);
        }
        calendarBody.appendChild(weekRow);
    }
    
    const dateCells = document.querySelectorAll("td");
    dateCells.forEach((cell) => {
        cell.addEventListener("click", function () {
            const date = new Date(currentDate);
            date.setDate(parseInt(this.textContent));
            displayTasks(date);
        });
    });
});
