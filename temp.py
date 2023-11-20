
import sqlite3

# Create a connection and cursor for interacting with the database
conn = sqlite3.connect('flight_booking.db')



class User:
    
    def __init__(self):
        self.conn = sqlite3.connect('flight_booking.db')
        self.cursor = self.conn.cursor()

    def login(self, username, password):
        self.cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        return self.cursor.fetchone() is not None

    def signup(self, username, password):
        try:
            self.cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        
    def view_bookings(self, user_id):
        self.cursor.execute('SELECT * FROM bookings WHERE user_id = ?', (user_id,))
        bookings = self.cursor.fetchall()
        return bookings  # Return bookings associated with the user
    
    def search_flight(self, search_criteria):
        self.cursor.execute('SELECT * FROM flights WHERE flight_name = ? OR flight_date = ? OR id = ? ', (search_criteria, search_criteria,search_criteria))
        return self.cursor.fetchall()

    def book_ticket(self, flight_id, user_id,no_of_tickets):
        # Check available seats for the selected flight
        self.cursor.execute(f'SELECT SUM(no_of_tickets) FROM bookings WHERE flight_id = {flight_id}')
        booked_seats = self.cursor.fetchone()[0]
        print(booked_seats)
        if booked_seats==None :
            booked_seats=0

        if booked_seats >= 60:
            return "Sorry, no seats available for this flight."

        # Book the ticket
        try:
            self.cursor.execute('INSERT INTO bookings (user_id, flight_id,no_of_tickets) VALUES (?, ?,?)', (user_id, flight_id,no_of_tickets))
            self.conn.commit()
            return "Ticket booked successfully!"
        except sqlite3.IntegrityError:
            return "Booking failed. Please try again."

 
    def __del__(self):
        self.conn.close()


class Admin:
    def __init__(self):
        self.conn = sqlite3.connect('flight_booking.db')
        self.cursor = self.conn.cursor()

    def add_admin_credentials(self, username, password):
        self.cursor.execute('INSERT INTO admins (username, password) VALUES (?, ?)', (username, password))
        self.conn.commit()


    def setup_admin(self):
        # Add admin credentials if not already present
        self.cursor.execute('SELECT * FROM admins')
        admin_data = self.cursor.fetchall()

        if not admin_data:  # If no admin data exists in the database
            admin_username = input("Enter admin username: ")
            admin_password = input("Enter admin password: ")

            self.add_admin_credentials(admin_username, admin_password)
            print("Admin credentials added successfully!")
        else:
            # print(admin_data)
            # print("Admin credentials which  exist.")
            print('Welcome to admin page')


    def login(self, username, password):
        self.cursor.execute('SELECT * FROM admins WHERE username = ? AND password = ?', (username, password))
        return self.cursor.fetchone() is not None

    def add_flight(self, flight_name, flight_date,flight_id,flight_from,flight_to):
        try:
            self.cursor.execute('INSERT INTO flights (id,flight_name, flight_date,flight_from,flight_to) VALUES (?, ?, ?,?,?)', (flight_id, flight_name, flight_date,flight_from,flight_to))
            self.conn.commit()
            return "Flight details added successfully"
        except sqlite3.IntegrityError:
            return False

    def view_bookings(self, filter_criteria):
        if filter_criteria == 'all':
            self.cursor.execute('SELECT * FROM bookings')
        elif filter_criteria == 'flight_id':
            flight_id = int(input("Enter Flight ID: "))
            self.cursor.execute('SELECT * FROM bookings WHERE flight_id = ?', (flight_id,))
        elif filter_criteria == 'flight_name':
            flight_name = input("Enter Flight Name: ")
            self.cursor.execute('''
                SELECT * FROM bookings 
                JOIN flights ON bookings.flight_id = flights.id 
                WHERE flights.flight_name = ?
            ''', (flight_name,))
        elif filter_criteria == 'date':
            flight_date = input("Enter Flight Date (YYYY-MM-DD): ")
            self.cursor.execute('SELECT * FROM bookings WHERE flight_id IN (SELECT id FROM flights WHERE flight_date = ?)', (flight_date,))
        else:
            return "Invalid filter criteria."

        bookings = self.cursor.fetchall()
        return bookings
    
    def __del__(self):
        self.conn.close()


class Flight:
    def __init__(self):
        self.conn = sqlite3.connect('flight_booking.db')
        self.cursor = self.conn.cursor()

    def search_flight(self, search_criteria):
        self.cursor.execute('SELECT * FROM flights WHERE flight_name = ? OR flight_date = ? OR id = ? ', (search_criteria, search_criteria,search_criteria))
        return self.cursor.fetchall()

    def book_ticket(self, flight_id, user_id,no_of_tickets):
        self.cursor.execute('SELECT SUM(no_of_tickets) FROM bookings WHERE flight_id = ?', (flight_id,))
        if booked_seats==None :
            booked_seats=0
        booked_seats = self.cursor.fetchone()[0]
        if booked_seats >= 60:
            return "Sorry, no seats available for this flight."

        

        try:
            self.cursor.execute('INSERT INTO bookings (user_id, flight_id,no_of_tickets) VALUES (?, ?,?)', (user_id, flight_id,no_of_tickets))
            self.conn.commit()
            return "Ticket booked successfully!"
        except sqlite3.IntegrityError:
            return "Booking failed. Please try again."

    def __del__(self):
        self.conn.close()


def user_interface():
    user = User()
    cursor = conn.cursor()

    while True:
        try:
            print("\nWelcome to the Flight Booking System")
            print("1. Login")
            print("2. Signup")
            print("3. Exit")
            choice = input("Enter choice: ")

            if choice == '1':  # User login
                username = input("Enter username: ")
                password = input("Enter password: ")

                if user.login(username, password):
                    print("Login successful!")
                    user_id = user.cursor.lastrowid  # Assuming user_id is obtained after successful login

                    while True:
                        print("\nUser Menu:")
                        print("1. Search Flights")
                        print("2. Book Ticket")
                        print("3. View My Bookings")
                        print("4. Logout")
                        user_choice = input("Enter choice: ")

                        if user_choice == '1':  # Search Flights
                            search_criteria = input("Enter flight name or date or flight id: ")
                            flights = user.search_flight(search_criteria)
                            if flights:
                                print("Matching flights:")
                                for flight in flights:
                                    print(flight)
                            else:
                                print("No flights found.")

                        elif user_choice == '2':  # Book Ticket
                            data=cursor.execute('''SELECT * FROM FLIGHTS''')
                            for row in data:
                                print(row)
                            flight_id = int(input("Enter Flight ID to book: "))
                            no_of_tickets = int(input("Enter no of tickets to book : "))
                            result = user.book_ticket(flight_id, user_id,no_of_tickets)
                            print(result)

                        elif user_choice == '3':  # View My Bookings
                            
                            bookings = user.view_bookings(user_id)
                            if bookings:
                                print("Your Bookings:")
                                for booking in bookings:
                                    print(booking)
                            else:
                                print("You have no bookings.")

                        elif user_choice == '4':  # Logout
                            del user
                            return

                        else:
                            print("Invalid choice.")

                else:
                    print("Invalid username or password. Try again.")

            elif choice == '2':  # Signup
                username = input("Enter new username: ")
                password = input("Enter new password: ")

                if user.signup(username, password):
                    print("Signup successful! Please login.")
                else:
                    print("Username already exists. Try a different username.")

            elif choice == '3':  # Exit
                return

            else:
                print("Invalid choice.")

        except Exception as e:
            print("An error occurred:", e)


def admin_interface():
    admin = Admin()
    admin.setup_admin()
    
    while True:
        try:
            print("\nAdmin Menu:")
            print("1. Login")
            print("2. Exit")
            choice = input("Enter choice: ")

            if choice == '1':  # Admin login
                username = input("Enter admin username: ")
                password = input("Enter admin password: ")

                if admin.login(username, password):
                    print("Admin Login successful!")

                    while True:
                        print("\nAdmin Options:")
                        print("1. Add Flight")
                        print("2. View Bookings")
                        print("3. Logout")
                        admin_choice = input("Enter choice: ")

                        if admin_choice == '1':  # Add Flight
                            flight_name = input("Enter flight name: ")
                            flight_date = input("Enter flight date (YYYY-MM-DD): ")
                            flight_id = input("Enter flight ID : ")
                            flight_from = input("Enter from location : ")
                            flight_to = input("Enter to location : ")
                            result = admin.add_flight(flight_name, flight_date,flight_id,flight_from,flight_to)
                            print(result)

                        elif admin_choice == '2':  # View Bookings
                            print("Filter Bookings:")
                            print("1. View all bookings")
                            print("2. View by Flight ID")
                            print("3. View by Flight Name")
                            print("4. View by Date")
                            filter_choice = input("Enter choice: ")

                            if filter_choice == '1':
                                bookings = admin.view_bookings('all')
                                if bookings:
                                    print("All Bookings:")
                                    for booking in bookings:
                                        print(booking)
                                else:
                                    print("No bookings found.")
                            
                            if filter_choice == '2':
                                bookings = admin.view_bookings('flight_id')
                                if bookings:
                                    print("All Bookings:")
                                    for booking in bookings:
                                        print(booking)
                                else:
                                    print("No bookings found.")
                            if filter_choice == '3':
                                bookings = admin.view_bookings('flight_name')
                                if bookings:
                                    print("All Bookings:")
                                    for booking in bookings:
                                        print(booking)
                                else:
                                    print("No bookings found.")
                            if filter_choice == '4':
                                bookings = admin.view_bookings('date')
                                if bookings:
                                    print("All Bookings:")
                                    for booking in bookings:
                                        print(booking)
                                else:
                                    print("No bookings found.")
                                

                        elif admin_choice == '3':  # Logout
                            del admin
                            return

                        else:
                            print("Invalid choice.")

                else:
                    print("Invalid admin credentials. Try again.")

            elif choice == '2':
                break
                
            else:
                print("Invalid choice.")

        except Exception as e:
            print("An error occurred:", e)

def createdb():
# Create tables for users, flights, and bookings
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')

            
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            flight_id INTEGER,
            no_of_tickets INTEGER,       
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (flight_id) REFERENCES flights(id)
        )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ADMINS(
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE,
        password TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS flights (
            id INTEGER PRIMARY KEY,
            flight_name TEXT,
            flight_date TEXT,
            flight_from TEXT,
            flight_to TEXT              
        )
    ''')




    conn.commit()



# Main program flow
createdb()
while True:
    try:
        print("\nMain Menu:")
        print("1. User")
        print("2. Admin")
        print("3. Exit")
        role_choice = input("Enter choice: ")

        if role_choice == '1':
            user_interface()
        elif role_choice == '2':
            admin_interface()
        elif role_choice == '3':
            break
        else:
            print("Invalid choice.")

    except Exception as e:
        print("An error occurred:", e)
