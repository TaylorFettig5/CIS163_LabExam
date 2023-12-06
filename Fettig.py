"""
Taylor Fettig
Lab Exam
12/06/2023
"""

from abc import ABC, abstractmethod
from typing import List


class Media(ABC):
    
    def __init__(self, title: str, genre: str, new_release: bool, quantity: int, out: int):
        
        self._title = title
        self._genre = genre
        self._new_release = new_release
        self._quantity = quantity
        self._out = out

    @property
    def title(self) -> str:
        return self._title

    @property
    def genre(self) -> str:
        return self._genre

    @property
    def quantity(self) -> int:
        return self._quantity

    @quantity.setter
    def quantity(self, num: int):
        self._quantity = num

    @property
    def out(self) -> int:
        return self._out

    @out.setter
    def out(self, num: int):
        self._out = num

    @property
    def new_release(self) -> bool:
        return self._new_release

    @new_release.setter
    def new_release(self, new_r: bool):
        self._new_release = new_r

    @abstractmethod
    def __str__(self):
        pass
    
    def __str__(self):
        return f"{self.title} - {self.genre}"

class Video(Media):
    def __init__(self, title: str, genre: str, new_release: bool, quantity: int = 5):
        super().__init__(title, genre, new_release, quantity, 0)  

    def __str__(self):
        return super().__str__()


class TV(Media):
    def __init__(self, title: str, genre: str, new_release: bool, quantity: int = 1):
        super().__init__(title, genre, new_release, quantity, 0) 
        self._season = 1
        self._episodes = 1

    @property
    def episodes(self) -> int:
        return self._episodes

    @episodes.setter
    def episodes(self, value: int):
        if value > 0:
            self._episodes = value
        else:
            raise ValueError("Episodes should be a positive integer.")

    @property
    def season(self) -> int:
        return self._season

    @season.setter
    def season(self, value: int):
        if value > 0:
            self._season = value
        else:
            raise ValueError("Season should be a positive integer.")

    def __str__(self):
        media_info = super().__str__()
        return f"{media_info}\nNumber of Seasons: {self.season}\nNumber of Episodes: {self.episodes}"


class VideoGame(Media):
    def __init__(self, title: str, genre: str, new_release: bool, console: str, quantity: int = 2):
        super().__init__(title, genre, new_release, quantity, 0) 
        self._console = console

    @property
    def console(self) -> str:
        return self._console

    @console.setter
    def console(self, value: str):
        self._console = value

    def __str__(self):
        media_info = super().__str__()
        return f"{media_info}\nConsole: {self.console}"


class Customer:

    def __init__(self, first_name, last_name, phone_number):
        self.__first_name = first_name
        self.__last_name = last_name
        self.__phone_num = phone_number
        self.__media = list()
        self.__history = list()

    @property
    def name(self) -> str:
        return f'{self.__last_name}, {self.__first_name}'

    @name.setter
    def name(self, name):
        names = name.split()
        self.__first_name = names[0]
        self.__last_name = names[1]

    @property
    def phone_number(self) -> str:
        return self.__phone_num

    @property
    def media(self) -> list:
        return self.__media

    def append_media(self, title: str):
        self.__media.append(title)

    @property
    def history(self) -> list:
        return self.__history

    def append_history(self, genre: str):
        self.__history.append(genre)


class Store:
    def __init__(self):
        self.__inventory = {}
        self.__customer = {}

    @property
    def inventory(self):
        return self.__inventory

    @property
    def customer(self):
        return self.__customer

    def add_stock(self, media: Media):
        if not isinstance(media, Media):
            raise ValueError("Invalid data type. Please provide a Media type.")

        title = media.title
        self.__inventory[title] = media

    def create_customer(self, customer: Customer):
        phone_number = customer.phone_number
        self.__customer[phone_number] = customer

    def check_out(self, title: str, phone_number: str):
        if phone_number not in self.__customer:
            raise InvalidCustomer("Customer does not exist.")

        if title not in self.__inventory:
            raise InvalidTitle("Title does not exist.")

        customer = self.__customer[phone_number]
        media = self.__inventory[title]

        if isinstance(media, VideoGame) and not self.check_limit(media, customer):
            raise TooManyVideoGames("Customer has already checked out 2 video games.")

        if media.quantity <= 0:
            return f"{title}-Checkout Failed! Not enough stock."

        customer.append_media(title)
        customer.append_history(media.genre)
        media.quantity -= 1

        return f"{title} - Checkout Successful!"

    def check_limit(self, media, customer):
        count = 0
        if isinstance(media, VideoGame):
            for i in customer.media:
                if isinstance(self.__inventory[i], VideoGame):
                    count += 1
        return count < 2

    def check_in(self, title: str, phone_number: str):
        if phone_number not in self.__customer or title not in self.__inventory:
            return f"{title} - Check in failed for {phone_number}."

        customer = self.__customer[phone_number]
        media = self.__inventory[title]

        if media.out <= 0:
            return f"{title} - Check in failed for {phone_number}."

        media.out -= 1

        return f"{title} - Checked in for {customer.name}."

    def recommend_media(self, phone_number: str) -> List[str] | str:
        if phone_number not in self.__customer:
            raise InvalidCustomer("Customer does not exist.")

        customer = self.__customer[phone_number]
        recommendations = []

        for title, media in self.__inventory.items():
            if media.genre in customer.history and title not in customer.media:
                recommendations.append(title)

        if not recommendations:
            return 'No recommendations'

        return recommendations


class TooManyVideoGames(Exception):

    def __init__(self, value):
        super().__init__(value)


class InvalidCustomer(Exception):

    def __init__(self, value):
        super().__init__(value)


class InvalidTitle(Exception):

    def __init__(self, value):
        super().__init__(value)
        
 
