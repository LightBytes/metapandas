"""This module defines a HooksManager class for handling (de)installation of decorators."""
import sys

from typing import Optional
from functools import partial

from metapandas.util import vprint, friendly_symbol_name, snake_case, mangle


class HooksManager:
    """A hooks class."""

    @classmethod
    def _generate_hook_flag_varname(cls):
        """Generate a variable name for keeping track of the installation of the hook decorators."""
        return "_{}_INSTALLED".format(snake_case(cls.__name__).upper())

    @classmethod
    def apply_hooks(
        cls,
        obj,
        decorator_function,
        hooks_dict,
        flag_var: Optional[str] = None,
        mangled_prefix: str = "",
        mangled_suffix: str = "_original",
    ) -> bool:
        """Apply hooks to obj using decorator_function.

        Parameters
        ----------
        obj: Any
            A mutable python module, class or function to decorate.
        decorator_function: Callable
            The decorator function to apply.
        hooks_dict: Dict[str, Dict[str, Any]]
            A dictionary of obj properties to modify with each
            entry defining a set of kwargs to use for the decorator_function.
        flag_var: str or None
            A handle to journal the hook installation/deinstallation.
        managed_prefix: str
            The prefix to use for a new handle to the original decorated property.
        mangled_suffix: str
            The suffix to use for a new handle to the original decorated property.

        Returns
        -------
        bool
            Indicator of whether hooks were successfully installed.

        """
        flag_var = flag_var or cls._generate_hook_flag_varname()
        # only apply decorators if not already done so
        # this prevents clobbering the original methods when called multiple times
        applied = False

        def not_found(obj_name, method_name, decorator_function, *args, **kwargs):
            raise AttributeError(
                "Unable to decorate {obj_name}.{method_name} with {decorator_function}"
                "".format(**locals())
            )

        if not getattr(obj, flag_var, None):
            for method_name, decorator_kwargs in hooks_dict.items():
                obj_name = friendly_symbol_name(obj)
                mangled_name = mangle(
                    prefix=mangled_prefix, name=method_name, suffix=mangled_suffix
                )
                if not hasattr(obj, method_name):
                    vprint(
                        "Unable to decorate {obj_name}.{method_name} with {decorator_function}"
                        "".format(**locals()),
                        file=sys.stderr,
                    )
                original_func = getattr(
                    obj,
                    method_name,
                    partial(not_found, obj_name, method_name, decorator_function),
                )
                setattr(
                    obj,
                    method_name,
                    decorator_function(original_func, **decorator_kwargs),
                )
                setattr(obj, mangled_name, original_func)
                vprint("Applied hook for {obj_name}.{method_name}".format(**locals()))
            # mark as installed
            setattr(obj, flag_var, True)
            applied = True
        return applied

    @classmethod
    def remove_hooks(
        cls,
        obj,
        hooks_dict,
        flag_var: Optional[str] = None,
        mangled_prefix: str = "",
        mangled_suffix: str = "_original",
    ):
        """Remove hooks from obj.

        Parameters
        ----------
        obj: Any
            A mutable python module, class or function to decorate.
        hooks_dict: Dict[str, Dict[str, Any]]
            A dictionary of obj modified properties.
        flag_var: str or None
            A handle to journal the hook installation/deinstallation.
        managed_prefix: str
            The prefix used for the original decorated property.
        mangled_suffix: str
            The suffix used for the original decorated property.

        Returns
        -------
        bool
            Indicator of whether hooks were successfully uninstalled.

        """
        flag_var = flag_var or cls._generate_hook_flag_varname()
        # only remove decorators if needed
        applied = False
        if getattr(obj, flag_var, None):
            for method_name in hooks_dict.keys():
                mangled_name = mangle(
                    prefix=mangled_prefix, name=method_name, suffix=mangled_suffix
                )
                setattr(obj, method_name, getattr(obj, mangled_name))
                try:
                    delattr(obj, method_name + "_original")
                except AttributeError:
                    setattr(obj, method_name + "_original", None)
            # mark as uninstalled
            try:
                delattr(obj, flag_var)
            except AttributeError:
                # can't delete as a class-level variable, so set to False instead
                setattr(obj, flag_var, False)
            applied = True
        return applied
