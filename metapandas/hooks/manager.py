class HooksManager:
    """A hooks class."""

    @classmethod
    def _generate_hook_flag_varname(cls):
        """Generate a variable name for keeping track of the installation of the hook decorators."""
        return "_{}_INSTALLED".format(re.sub(r'(?<!^)(?=[A-Z])', '_', cls.__name__).upper())

    @classmethod
    def apply_hooks(cls, obj, decorator_function, hooks_dict,
                    flag_var: Optional[str] = None,
                    mangled_prefix: str = '', mangled_suffix: str = '_original'):
        flag_var = flag_var or cls._generate_hook_flag_varname()
        # only apply decorators if not already done so
        # this prevents clobbering the original methods when called multiple times        
        applied = False
        if not getattr(obj, flag_var, None):
            for method_name, decorator_kwargs in hooks_dict.items():
                original_func = getattr(obj, method_name)
                setattr(obj, method_name, decorator_function(original_func, **decorator_kwargs))
                mangled_name = '{}{}{}'.format(mangled_prefix, method_name, mangled_suffix)
                setattr(obj, mangled_name, original_func)
                obj_name = obj.__name__ if str(type(obj)) == "<class 'module'>" else obj
                print('Applied hook for {}.{}'.format(re.sub("(<class '|'>)", '', str(obj_name)), method_name))
            # mark as installed
            setattr(obj, flag_var, True)
            applied = True
        return applied
    
    @classmethod
    def remove_hooks(cls, obj, hooks_dict, flag_var: Optional[str] = None,
                     mangled_prefix: str = '', mangled_suffix: str = '_original'):
        flag_var = flag_var or cls._generate_hook_flag_varname()
        # only remove decorators if needed
        applied = False
        if getattr(obj, flag_var, None):
            for method_name in hooks_dict.keys():
                mangled_name = '{}{}{}'.format(mangled_prefix, method_name, mangled_suffix)
                setattr(obj, method_name, getattr(obj, mangled_name))
                try:
                    delattr(obj, method_name + '_original')
                except AttributeError:
                    setattr(obj, method_name + '_original', None)
            # mark as uninstalled
            try:
                delattr(obj, flag_var)
            except AttributeError:
                # can't delete as a class-level variable, so set to False instead
                setattr(obj, flag_var, False)
            applied = True
        return applied