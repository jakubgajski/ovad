from functools import cache
import inspect
from typing import Callable


class ArgumentsDispatcher(dict):
    """
    This class stores overloaded methods and provides dispatching functionality based on arguments hashes.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def register(self, obj: Callable) -> None:
        """
        Stores overloaded method. obj is a callable to be stored.

        Parameters
        ----------
        obj: Callable

        Returns
        -------
        None
        """
        sig = inspect.Signature.from_callable(obj, follow_wrapped=False)

        super().__setitem__(sig, obj)

    def __setitem__(self, key, value):
        """
        Sets an item in the dictionary. This method is used to store an overloaded method.

        Parameters
        ----------
        key: Any
            The key to be used for storing the value. This is not actually used in this implementation.
        value: Callable
            The value to be stored. This should be a callable object.

        Returns
        -------
        None
        """
        self.register(value)

    @cache
    def find_signature(self, *args, **kwargs) -> inspect.Signature:
        """
        Finds the overloaded method based on the arguments passed.

        Parameters
        ----------
        args
        kwargs

        Returns
        -------
        Callable

        Raises
        ------
        TypeError
        """
        for sig in self:
            try:
                sig.bind(*args, **kwargs)
                return sig
            except TypeError:
                pass

        raise TypeError("No overloaded method found for provided arguments.")


    def __call__(self, *args, **kwargs):
        """
        Calls the overloaded method based on the arguments passed.

        Parameters
        ----------
        args
        kwargs

        Returns
        -------
        Any
        """
        sig = self.find_signature(*args, **kwargs)
        return self[sig](*args, **kwargs)


class DispatchedDict(dict):
    """
    This class provides dispatching functionality based on arguments hashes.
    """

    def __setitem__(self, key, value):
        self.setdefault(key, ArgumentsDispatcher()).register(value)


class OvadMeta(type):
    """
    Metaclass providing overloading functionality for Ovad.
    """

    @classmethod
    def __prepare__(metacls, name, bases):
        return DispatchedDict()

    def __new__(metacls, name, bases, namespace, **kwargs):
        """
        Creates new class with overloaded methods.
        """
        print(namespace)
        return type.__new__(metacls, name, bases, namespace)