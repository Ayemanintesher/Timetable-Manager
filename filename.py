# File: timetable_manager.py
# Author: Ayeman Mohammad Intesher
# Student ID: 110421226
# Email ID: intay002@mymail.unisa.edu.au
# This is my own work as defined by the University's Academic Misconduct Policy.

def main():
    """Main function to run the program."""

    # Print program header and author details
    print("Timetable Manager")
    print("Author: Ayeman Mohammad Intesher")
    print("Email: intay002@mymail.unisa.edu.au")
    
     # Initialize the timetable and set the default starting day
    timetable = initialize_timetable()
    start_day = "Monday"
    
    # Flag to continue running the program
    continue_program = True

    # Main loop to keep displaying the menu and taking user input
    while continue_program:
        try:
             # Display the main menu and get the user's choice
            choice = display_menu()      

             # Execute the corresponding action based on the user's choice               
            if choice == "1":
                create_event(timetable)
            elif choice == "2":
                update_event(timetable)
            elif choice == "3":
                delete_event(timetable)
            elif choice == "4":
                print_timetable(timetable, start_day)
            elif choice == "5":
                print_events_for_day(timetable)
            elif choice == "6":
                search_events(timetable, start_day)
            elif choice == "7":
                start_day = set_starting_day()
            elif choice == "8":
                save_timetable(timetable)
            elif choice == "9":
                timetable = load_timetable()
            elif choice == "10":
                print("Exiting")
                continue_program = False
            else:
                #If the choice is not one of the valid options, raise a ValueError
                raise ValueError
        except ValueError:
            print("Invalid choice. Please try again.")


def initialize_timetable():     #This function initializes an empty timetable with days of the week as keys and empty lists as values.
    """Initialize an empty timetable."""  
    timetable = {}
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    for day in days:
        timetable[day] = []
        
    return timetable


def display_menu():
    """Display the main menu and return the user's choice."""          
    
    # Display the main menu options
    print("\nMenu")
    print("1. Create an event")
    print("2. Update an event")
    print("3. Delete an event")
    print("4. Print the timetable")
    print("5. Print events for a specific day")
    print("6. Search for events")
    print("7. Set starting day of the week")
    print("8. Save timetable to a file")
    print("9. Load timetable from a file")
    print("10.Exit")
    print()
    return input("Enter your choice: ")



def create_event(timetable):
    """Create a new event."""

    # Prompt the user to input the day for the event
    day = input_day() 
    title = input("Enter event title: ")
    start_time = input_time("Enter start time (e.g., 9am or 5:00pm): ")
    end_time = input_time("Enter end time (e.g., 11am or 3:30pm): ")
    location = input("Enter location (optional): ")

    # Check if the new event overlaps with any existing events on the chosen day
    if is_overlapping(start_time, end_time, timetable[day]):
        print("Event overlaps with another event. Please reschedule.")
        return
    
    # Create a dictionary to represent the event
    event = {
        "title": title,
        "start": start_time,
        "end": end_time,
        "location": location
    }

    # Add the new event to the timetable for the chosen day
    timetable[day].append(event)

     # Sort the events on the chosen day by their start times
    timetable[day].sort(key=lambda x: x["start"])

    # Notify the user that the event has been added
    print(f"Event added on {day} from {start_time} to {end_time}.")




def update_event(timetable):
    """Update an existing event based on the user's choice (start time or keyword)."""

    # Prompt the user to input the day of the event they wish to update
    day = input_day()
    continue_choice=True
    while continue_choice:

        # Prompt the user to choose the update criteria: by start time or by keyword
        choice = input('Enter "a" to update by start time or "b" to update by keyword: ').lower()

        # if choice == 'a':
        #     # Update by start time
        #     start_time = input_time("Enter start time of the event to update (e.g., 9am or 5:00pm): ")
        #     matching_events = [event for event in timetable[day] if event["start"] == start_time]  #List Comprenhension
        
            # Check if the user's choice is 'a'
        if choice == 'a':
            # Prompt the user to enter the start time of the event they want to update
            start_time = input("Enter the start time of the event to update (e.g., 9am or 5:00pm): ")

            # Create a list called 'matching_events' to store events with the same start time
            matching_events = []

            # Iterate through all events in the timetable for the specified 'day'
            for event in timetable[day]:
                # Check if the start time of the current event matches the user-provided start_time
                if event["start"] == start_time:
                    # If it matches, add the event to the 'matching_events' list
                    matching_events.append(event)
                    continue_choice=False
        # At this point, 'matching_events' contains a list of events that have the same start time as provided by the user

        elif choice == 'b':
            # Update by keyword
            keyword = input("Enter keyword related to the event: ").lower()
            matching_events = [event for event in timetable[day] if keyword in event['title'].lower() or keyword in event['location'].lower()] #List Comprenhension
            
            # Create a list called 'matching_events' to store events containing the keyword
            matching_events = []

            # Iterate through all events in the timetable for the specified 'day'
            for event in timetable[day]:
                # Check if the keyword is present in either the event title or location, case-insensitively
                if keyword in event['title'].lower() or keyword in event['location'].lower():
                    # If the keyword is found, add the event to the 'matching_events' list
                    matching_events.append(event)
                    continue_choice=False
        else:
            # Invalid choice
            print("Invalid choice. Please enter 'a' to update by start time or 'b' to update by keyword.")
            

    # If no matching events are found, notify the user and return
    if not matching_events:
        print("No matching event found.")
        return

    # Iterate through the matching events
    for event in matching_events:
        print(f"Updating event: {event['title']} from {event['start']} to {event['end']}")

        # Prompt the user to input the updated details for the event
        title = input("Enter new event title: ")
        new_start_time = input_time("Enter new start time (e.g., 9am or 5:00pm): ")
        new_end_time = input_time("Enter new end time (e.g., 11am or 3:30pm): ")
        location = input("Enter new location (optional): ")

        # Create a temporary list excluding the current event to check for overlaps
        # temp_timetable = [e for e in timetable[day] if e["start"] != event["start"]] #list comprehension

        
        # Create a temporary list called 'temp_timetable' to exclude the current event
        temp_timetable = []

        # Iterate through all events in the timetable for the specified 'day'
        for e in timetable[day]:
            # Check if the start time of the current event is not equal to the start time of the event being updated
            if e["start"] != event["start"]:
                # If they have different start times, add the current event to the 'temp_timetable' list
                temp_timetable.append(e)

        # Check if the updated event overlaps with any other events on the specified day
        if is_overlapping(new_start_time, new_end_time, temp_timetable):
            print("Event overlaps with another event. Please reschedule.")
            return

        # Update the event details in the timetable
        event["title"] = title
        event["start"] = new_start_time
        event["end"] = new_end_time
        event["location"] = location

        # Sort the events on the specified day by their start times
        timetable[day].sort(key=lambda x: x["start"])

        # Notify the user that the event has been updated
        print(f"Event on {day} updated.")




def time_to_minutes(time_str):
    """Convert a time string like '9am' or '5:30pm' to minutes since midnight."""

    # Initialize hours and minutes to zero
    hours = 0
    minutes = 0

    # Check if the time string has "am"
    if "am" in time_str:
        time_str = time_str.replace("am","")

        # Check if the time string has minutes (i.e., a colon)
        if ":" in time_str:
            # Split hours and minutes and convert them to integers
            split_time = time_str.split(":")
            hours = int(split_time[0])  #indexing as split_time is list (for accessing list you need indexing)
            minutes = int(split_time[1])
        else:
            # If no minutes, convert the entire string to hours
            hours = int(time_str)

    # If the time string has "pm"
    else:
        time_str = time_str.replace("pm", "")

        # Check if the time string has minutes
        if ":" in time_str:
            # Split hours and minutes and convert them to integers
            split_time = time_str.split(":")
            hours = int(split_time[0])
            minutes = int(split_time[1])

            # Add 12 hours for PM time unless it's 12 PM
            if hours != 12:
                hours += 12
        else:
            # If no minutes, convert the entire string to hours
            hours = int(time_str)
            
            # Add 12 hours for PM time unless it's 12 PM
            if hours != 12:
                hours += 12

    # Convert total time to minutes since midnight
    total_minutes = (hours * 60) + minutes

    return total_minutes



def is_overlapping(start, end, events):
    """Check if the given time range overlaps with any event in the list."""
    # Convert start and end times to minutes.
    new_start_minutes = time_to_minutes(start)
    new_end_minutes = time_to_minutes(end)

    # Iterate over each event in the list.
    for event in events:
         # Convert event start and end times to minutes.
        event_start_minutes = time_to_minutes(event["start"])
        event_end_minutes = time_to_minutes(event["end"])
        
         # Check three possible overlapping scenarios:
        # 1. Start time of the new event is within the existing event.
        # 2. End time of the new event is within the existing event.
        # 3. The new event entirely spans the existing event.
        if (new_start_minutes >= event_start_minutes and new_start_minutes < event_end_minutes) or \
           (new_end_minutes > event_start_minutes and new_end_minutes <= event_end_minutes) or \
           (new_start_minutes <= event_start_minutes and new_start_minutes >= event_end_minutes):
            return True
            
    return False



def delete_event(timetable):
    """Delete an event."""

    # Prompt the user to input the day of the event they wish to delete
    day = input_day()
    continue_choice=True
    while continue_choice:
    
        # Prompt the user to choose the delete criteria: by start time or by keyword
        choice = input('Enter "a" to delete by start time or "b" to delete by keyword: ').lower()

        # If the user chooses to delete by start time
        if choice == 'a':
            # Prompt the user to input the start time of the event they wish to delete
            start_time = input_time("Enter start time of the event to delete (e.g., 9am or 5:00pm): ")

            # Iterate through the events on the specified day
            for event in timetable.get(day, []):
                if event["start"] == start_time:
                    # Remove the event from the timetable
                    timetable[day].remove(event)

                    # Notify the user that the event has been deleted
                    print(f"Event on {day} from {start_time} to {event['end']} titled '{event['title']}' at location '{event['location']}' deleted.")
                    continue_choice=False

                    
        # If the user chooses to delete by keyword
        elif choice == 'b':
            # Prompt the user to input a keyword related to the event they wish to delete
            keyword = input("Enter keyword related to the event: ").lower()

            # Iterate through the events on the specified day
            for event in timetable.get(day, []):
                if keyword in event['title'].lower() or keyword in event['location'].lower():
                    # Remove the event from the timetable
                    timetable[day].remove(event)

                    # Notify the user that the event has been deleted
                    print(f"Event on {day} titled '{event['title']}' at location '{event['location']}' deleted.")
                    continue_choice=False
                    
    # If no matching event is found based on the chosen criteria, notify the user
    print(f"No event found on {day} with the chosen criteria.")
    return


def input_day():
    """Prompt the user to input a day and validate it."""

    # List of valid days
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    # Continuously prompt the user for input until a valid day is provided
    while True:
        day = input("Enter day (Monday, Tuesday, Wednesday,Thursday, Friday, Saturday, Sunday): ")

        # If the input day is in the list of valid days, return it
        if day in days:
            return day
        
        # If the input day is not valid, notify the user and prompt again
        print("Invalid day. Please follow the correct format and try again.")



def is_valid_time(time):
    """Check if the provided time string is in a valid 12-hour format."""

    # Check if the time string ends with 'am' or 'pm'
    if time[-2:] not in ['am', 'pm']:
        return False
    
    # Remove the 'am' or 'pm' suffix
    time = time[:-2]

    # If the time string contains a colon (indicating minutes)
    if ':' in time:
        hour, minute = time.split(':')

        # Check if both hour and minute parts are digits
        if not hour.isdigit() or not minute.isdigit():
            return False
        
        # Check if the hour is between 1 and 12 and minute is between 0 and 59
        if int(hour) < 1 or int(hour) > 12 or int(minute) < 0 or int(minute) > 59:
            return False
    else:
        # If the time string does not contain a colon, check if it's a valid hour between 1 and 12
        if not time.isdigit() or int(time) < 1 or int(time) > 12:
            return False
    return True



def input_time(prompt):
    """Prompt the user to input a time and validate it using the 12-hour format."""

    # Continuously prompt the user for input until a valid time is provided
    while True:
        time = input(prompt)
        if is_valid_time(time):
            return time
        else:
            print("Invalid time format. Please follow the 12-hour format (e.g., 9am or 5:00pm). Please try again.")


      
def print_timetable(timetable, start_day):
    """ Print the timetable for the entire week starting from the specified day.."""

    # Rotate the list of days based on the starting day
    days = rotate_days(start_day)   

    # Iterate through the rotated list of days and print the events for each day
    for day in days:
        print(day)
        print('-' * 40)

        # Sort the events on the current day by their start times
        timetable[day].sort(key=lambda x: time_to_minutes(x["start"]))

        for event in timetable[day]:
            print(f"{event['start']} - {event['end']} : {event['title']} ({event['location']})")
        print()



def print_events_for_day(timetable):
    """Print events for a specific day."""

    # Prompt the user to input the day for which they want to see the events
    day = input_day()

    # Retrieve the events for the specified day
    events = timetable[day]

    # If there are no events for the specified day, notify the user
    if not events:
        print(f"No events scheduled for {day}.")
        return
    
    # Print each event for the specified day    
    for event in events:
        print(f"{event['start']} - {event['end']} : {event['title']} ({event['location']})")



def save_timetable(timetable):
    """Save the timetable to a file."""

    # Prompt the user to input the filename where they want to save the timetable
    filename = input("Enter filename to save: ")

    # Open the specified file in write mode
    with open(filename, 'w') as file:
        # Iterate through each day and its events in the timetable
        for day, events in timetable.items():
            for event in events:
                # Write each event to the file in a comma-separated format
                file.write(f"{day},{event['start']},{event['end']},{event['title']},{event['location']}\n")

    # Notify the user that the timetable has been saved
    print(f"Timetable saved to {filename}.")



def load_timetable():
    """Load the timetable from a file."""

    # Prompt the user to input the filename from which they want to load the timetable
    filename = input("Enter filename to load: ")

    try:
        # Open the specified file in read mode
        with open(filename, 'r') as file:
            # Read all lines from the file
            lines = file.readlines()

            # Initialize an empty timetable
            timetable = initialize_timetable()

            # Process each line from the file
            for line in lines:
                # Split the line into its components
                day, start, end, title, location = line.strip().split(',')

                # Add the event to the timetable
                timetable[day].append({
                    "start": start,
                    "end": end,
                    "title": title,
                    "location": location
                })

            # Notify the user that the timetable has been loaded
            print(f"Timetable loaded from {filename}.")
            return timetable
    except FileNotFoundError:
        # If the specified file is not found, notify the user and return an initialized empty timetable
        print(f"File {filename} not found.")
        return initialize_timetable()



# Advanced Features



def set_starting_day():
    """Set the starting day of the week."""

    # List of valid days
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    # Display the days for the user to choose from
    print("\nChoose the starting day of the week:")
    i=1
    for day in days:
        print(f"{i}. {day}")
        i+=1

    # Continuously prompt the user for input until a valid choice is provided
    while True:
        choice = input("Enter your choice (1-7): ")

        # Check if the choice is a digit and within the valid range
        if choice.isdigit() and 1 <= int(choice) <= 7:    # Validate if the choice is between 1 and 7
            return days[int(choice) - 1]
        
        # If the choice is not valid, notify the user and prompt again
        print("Invalid choice. Please try again.")    



def rotate_days(start_day):
    """Rotate the list of days based on the starting day."""

    # List of valid days
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    # Rotate the list until the starting day is at the beginning
    while days[0] != start_day:
        days.append(days.pop(0))
    return days



def search_events(timetable, start_day):
    """Search for events based on keywords in their title or location."""

    # Prompt the user to input a keyword to search for
    keyword = input("Enter keyword to search: ").lower()

    results = []
    # Rotate the list of days based on the starting day
    days = rotate_days(start_day)

    # Search for events that match the keyword in their title or location
    for day in days:
        for event in timetable[day]:
            if keyword in event['title'].lower() or keyword in event['location'].lower():
                results.append((day, event))

    # If no matching events are found, notify the user
    if not results:
        print("No events found.")
        return
    
    # Print each matching event
    for day, event in results:
        print(f"{day} - {event['start']} to {event['end']} : {event['title']} ({event['location']})")


if __name__ == "__main__":
    main()


    