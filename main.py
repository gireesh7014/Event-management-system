import json
import os
from abc import ABC, abstractmethod
from datetime import datetime
import uuid

class User(ABC):
    def __init__(self, user_id, username, password, email):
        self.user_id = user_id
        self.username = username
        self.password = password  
        self.email = email
        self.is_active = True

    def update_profile(self, username=None, email=None):
        if username:
            self.username = username
        if email:
            self.email = email
        return True
    
    @abstractmethod
    def get_role(self):
        pass
    
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "password": self.password,
            "email": self.email,
            "is_active": self.is_active,
            "role": self.get_role()
        }
    
    @classmethod
    def from_dict(cls, data):
        if data["role"] == "admin":
            return Admin(data["user_id"], data["username"], data["password"], data["email"])
        elif data["role"] == "organizer":
            org = Organizer(data["user_id"], data["username"], data["password"], data["email"])
            org.events = data.get("events", [])
            return org
        else:
            user = RegularUser(data["user_id"], data["username"], data["password"], data["email"])
            user.registered_events = data.get("registered_events", [])
            return user


class Admin(User):
    def __init__(self, user_id, username, password, email):
        super().__init__(user_id, username, password, email)
    
    def get_role(self):
        return "admin"


class Organizer(User):
    def __init__(self, user_id, username, password, email):
        super().__init__(user_id, username, password, email)
        self.events = []  # List of event IDs created by this organizer
    
    def get_role(self):
        return "organizer"
    
    def add_event(self, event_id):
        self.events.append(event_id)
    
    def remove_event(self, event_id):
        if event_id in self.events:
            self.events.remove(event_id)
    
    def to_dict(self):
        data = super().to_dict()
        data["events"] = self.events
        return data


class RegularUser(User):
    def __init__(self, user_id, username, password, email):
        super().__init__(user_id, username, password, email)
        self.registered_events = []  # List of event IDs the user has registered for
    
    def get_role(self):
        return "user"
    
    def register_for_event(self, event_id):
        self.registered_events.append(event_id)
        return True
    
    def unregister_from_event(self, event_id):
        if event_id in self.registered_events:
            self.registered_events.remove(event_id)
            return True
        return False
    
    def to_dict(self):
        data = super().to_dict()
        data["registered_events"] = self.registered_events
        return data


class Event:
    def __init__(self, event_id, title, description, date, venue, capacity, category, organizer_id):
        self.event_id = event_id
        self.title = title
        self.description = description
        self.date = date  # datetime object
        self.venue = venue
        self.capacity = capacity
        self.category = category
        self.organizer_id = organizer_id
        self.is_approved = False
        self.registered_users = []  # List of user IDs registered for this event
    
    def register_user(self, user_id):
        if len(self.registered_users) < self.capacity:
            self.registered_users.append(user_id)
            return True
        return False
    
    def unregister_user(self, user_id):
        if user_id in self.registered_users:
            self.registered_users.remove(user_id)
            return True
        return False
    
    def approve_event(self):
        self.is_approved = True
        return True
    
    def is_full(self):
        return len(self.registered_users) >= self.capacity
    
    def seats_available(self):
        return self.capacity - len(self.registered_users)
    
    def to_dict(self):
        return {
            "event_id": self.event_id,
            "title": self.title,
            "description": self.description,
            "date": self.date.isoformat(),
            "venue": self.venue,
            "capacity": self.capacity,
            "category": self.category,
            "organizer_id": self.organizer_id,
            "is_approved": self.is_approved,
            "registered_users": self.registered_users
        }
    
    @classmethod
    def from_dict(cls, data):
        event = cls(
            data["event_id"],
            data["title"],
            data["description"],
            datetime.fromisoformat(data["date"]),
            data["venue"],
            data["capacity"],
            data["category"],
            data["organizer_id"]
        )
        event.is_approved = data["is_approved"]
        event.registered_users = data["registered_users"]
        return event


class DataStorage:
    def __init__(self, users_file="users.json", events_file="events.json"):
        self.users_file = users_file
        self.events_file = events_file
    
    def save_users(self, users):
        # Convert users to dictionary of dictionaries
        user_dicts = {uid: user.to_dict() for uid, user in users.items()}
        with open(self.users_file, 'w') as f:
            json.dump(user_dicts, f, indent=2)
    
    def load_users(self):
        if not os.path.exists(self.users_file):
            return {}
        
        try:
            with open(self.users_file, 'r') as f:
                user_dicts = json.load(f)
            
            # Convert back to User objects
            users = {}
            for uid, user_data in user_dicts.items():
                users[uid] = User.from_dict(user_data)
            
            return users
        except Exception as e:
            print(f"Error loading users: {e}")
            return {}
    
    def save_events(self, events):
        # Convert events to dictionary of dictionaries
        event_dicts = {eid: event.to_dict() for eid, event in events.items()}
        with open(self.events_file, 'w') as f:
            json.dump(event_dicts, f, indent=2)
    
    def load_events(self):
        if not os.path.exists(self.events_file):
            return {}
        
        try:
            with open(self.events_file, 'r') as f:
                event_dicts = json.load(f)
            
            # Convert back to Event objects
            events = {}
            for eid, event_data in event_dicts.items():
                events[eid] = Event.from_dict(event_data)
            
            return events
        except Exception as e:
            print(f"Error loading events: {e}")
            return {}


class UserManager:
    def __init__(self, storage):
        self.storage = storage
        self.users = self.storage.load_users()
    
    def add_user(self, username, password, email, role):
        # Check if username already exists
        for user in self.users.values():
            if user.username == username:
                return None, "Username already exists"
        
        user_id = str(uuid.uuid4())
        
        if role == "admin":
            user = Admin(user_id, username, password, email)
        elif role == "organizer":
            user = Organizer(user_id, username, password, email)
        else:  # default to regular user
            user = RegularUser(user_id, username, password, email)
        
        self.users[user_id] = user
        self._save_users()
        return user_id, "User created successfully"
    
    def get_user(self, user_id):
        return self.users.get(user_id)
    
    def authenticate(self, username, password):
        for user_id, user in self.users.items():
            if user.username == username and user.password == password and user.is_active:
                return user_id
        return None
    
    def delete_user(self, user_id):
        if user_id in self.users:
            del self.users[user_id]
            self._save_users()
            return True
        return False
    
    def get_all_users(self):
        return self.users
    
    def get_users_by_role(self, role):
        return {uid: user for uid, user in self.users.items() if user.get_role() == role}
    
    def _save_users(self):
        self.storage.save_users(self.users)


class EventManager:
    def __init__(self, storage):
        self.storage = storage
        self.events = self.storage.load_events()
    
    def create_event(self, title, description, date, venue, capacity, category, organizer_id):
        # Check if event date is not before today
        if date < datetime.now():
            return None, "Event date cannot be before today"
        
        event_id = str(uuid.uuid4())
        event = Event(event_id, title, description, date, venue, capacity, category, organizer_id)
        self.events[event_id] = event
        self._save_events()
        return event_id, "Event created successfully"
    
    def get_event(self, event_id):
        return self.events.get(event_id)
    
    def approve_event(self, event_id):
        event = self.get_event(event_id)
        if event:
            event.approve_event()
            self._save_events()
            return True
        return False
    
    def delete_event(self, event_id):
        if event_id in self.events:
            del self.events[event_id]
            self._save_events()
            return True
        return False
    
    def get_all_events(self):
        return self.events
    
    def get_approved_events(self):
        return {eid: event for eid, event in self.events.items() if event.is_approved}
    
    def get_unapproved_events(self):
        return {eid: event for eid, event in self.events.items() if not event.is_approved}
    
    def get_events_by_organizer(self, organizer_id):
        return {eid: event for eid, event in self.events.items() if event.organizer_id == organizer_id}
    
    def get_events_by_category(self, category):
        return {eid: event for eid, event in self.events.items() if event.category == category and event.is_approved}
    
    def get_events_sorted_by_date(self, ascending=True):
        sorted_events = sorted(self.events.values(), key=lambda e: e.date, reverse=not ascending)
        return {event.event_id: event for event in sorted_events if event.is_approved}
    
    def register_user_for_event(self, event_id, user_id):
        event = self.get_event(event_id)
        if event and not event.is_full() and event.is_approved:
            success = event.register_user(user_id)
            if success:
                self._save_events()
            return success
        return False
    
    def unregister_user_from_event(self, event_id, user_id):
        event = self.get_event(event_id)
        if event:
            success = event.unregister_user(user_id)
            if success:
                self._save_events()
            return success
        return False
    
    def get_events_for_user(self, user_id):
        return {eid: event for eid, event in self.events.items() 
                if user_id in event.registered_users and event.is_approved}
    
    def _save_events(self):
        self.storage.save_events(self.events)


class EventManagementSystem:
    def __init__(self, storage=None):
        if storage is None:
            storage = DataStorage()
        
        self.storage = storage
        self.user_manager = UserManager(storage)
        self.event_manager = EventManager(storage)
        
        # Create a default admin user if no users exist
        if not self.user_manager.get_users_by_role("admin"):
            self.user_manager.add_user("admin", "admin123", "admin@example.com", "admin")
    
    def login(self, username, password):
        user_id = self.user_manager.authenticate(username, password)
        if user_id:
            user = self.user_manager.get_user(user_id)
            return user_id, user.get_role()
        return None, None
    
    def register_user(self, username, password, email, role="user"):
        return self.user_manager.add_user(username, password, email, role)
    
    def create_event(self, title, description, date, venue, capacity, category, organizer_id):
        event_id, msg = self.event_manager.create_event(title, description, date, venue, capacity, category, organizer_id)
        if event_id:
            organizer = self.user_manager.get_user(organizer_id)
            if organizer and isinstance(organizer, Organizer):
                organizer.add_event(event_id)
                self.storage.save_users(self.user_manager.users)
        return event_id, msg
    
    def approve_event(self, event_id, admin_id):
        admin = self.user_manager.get_user(admin_id)
        if admin and admin.get_role() == "admin":
            return self.event_manager.approve_event(event_id)
        return False
    
    def register_for_event(self, event_id, user_id):
        user = self.user_manager.get_user(user_id)
        if user and user.get_role() == "user" and isinstance(user, RegularUser):
            success = self.event_manager.register_user_for_event(event_id, user_id)
            if success:
                user.register_for_event(event_id)
                self.storage.save_users(self.user_manager.users)
            return success
        return False
    
    def unregister_from_event(self, event_id, user_id):
        user = self.user_manager.get_user(user_id)
        if user and user.get_role() == "user" and isinstance(user, RegularUser):
            success = self.event_manager.unregister_user_from_event(event_id, user_id)
            if success:
                user.unregister_from_event(event_id)
                self.storage.save_users(self.user_manager.users)
            return success
        return False
    
    def delete_user(self, target_user_id, admin_id):
        admin = self.user_manager.get_user(admin_id)
        if not admin or admin.get_role() != "admin":
            return False, "Only admin can delete users"
        
        user = self.user_manager.get_user(target_user_id)
        if not user:
            return False, "User not found"
        
        # If deleting an organizer, delete all their events
        if user.get_role() == "organizer" and isinstance(user, Organizer):
            organizer_events = self.event_manager.get_events_by_organizer(target_user_id)
            for event_id in list(organizer_events.keys()):
                # Unregister all users from this event
                event = self.event_manager.get_event(event_id)
                for registered_user_id in list(event.registered_users):
                    registered_user = self.user_manager.get_user(registered_user_id)
                    if registered_user and isinstance(registered_user, RegularUser):
                        registered_user.unregister_from_event(event_id)
                # Delete the event
                self.event_manager.delete_event(event_id)
        
        # If deleting a user, unregister them from all events
        elif user.get_role() == "user" and isinstance(user, RegularUser):
            for event_id in list(user.registered_events):
                self.event_manager.unregister_user_from_event(event_id, target_user_id)
        
        # Finally delete the user
        self.user_manager.delete_user(target_user_id)
        return True, "User deleted successfully"
    
    def get_available_events(self, user_id=None, category=None, sort_by_date=False):
        events = self.event_manager.get_approved_events()
        
        if category:
            events = {eid: event for eid, event in events.items() if event.category == category}
        
        if sort_by_date:
            sorted_events = sorted(events.values(), key=lambda e: e.date)
            events = {event.event_id: event for event in sorted_events}
        
        return events
    
    def get_user_registrations(self, user_id):
        user = self.user_manager.get_user(user_id)
        if user and user.get_role() == "user" and isinstance(user, RegularUser):
            return user.registered_events
        return []
    
    def get_event_registrations(self, event_id, organizer_id=None):
        event = self.event_manager.get_event(event_id)
        if not event:
            return []
        
        # Check if the requesting user is the organizer of this event
        if organizer_id and event.organizer_id != organizer_id:
            return []
        
        return event.registered_users
    
    def get_user_events(self, organizer_id):
        return self.event_manager.get_events_by_organizer(organizer_id)
    
    def update_event(self, event_id, title, description, date, venue, capacity, category, organizer_id):
        """
        Update an existing event.
        Only the organizer of the event can update it.
        
        Args:
            event_id: ID of the event to update
            title: New event title
            description: New event description
            date: New event date (datetime object)
            venue: New event venue
            capacity: New event capacity
            category: New event category
            organizer_id: ID of the user attempting to update the event
            
        Returns:
            Tuple of (success, message)
        """
        # Get the event
        event = self.event_manager.get_event(event_id)
        if not event:
            return False, "Event not found"
        
        # Check if user is authorized to update this event
        if event.organizer_id != organizer_id:
            return False, "You can only edit your own events"
        
        # Check if capacity can be changed (can't reduce below current registrations)
        if capacity < len(event.registered_users):
            return False, f"Cannot reduce capacity below current registrations ({len(event.registered_users)})"
        
        # Update event details
        event.title = title
        event.description = description
        event.date = date
        event.venue = venue
        event.capacity = capacity
        event.category = category
        
        # Events may need re-approval after significant changes
        # Uncomment the following line if you want edited events to require re-approval
        # event.is_approved = False
        
        # Save changes
        self.event_manager.save_events()
        
        return True, "Event updated successfully"


