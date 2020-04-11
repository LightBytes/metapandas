"""Defines MetaDataFrame class, which extends pandas.DataFrame."""
import pandas as pd


class MetaDataFrame(pd.DataFrame):
    """A specialised DataFrame class for tracking metadata.

    Examples
    --------
    >>> from metapandas.metadataframe import MetaDataFrame
    >>> mdf = MetaDataFrame([[1, 2, 3]], columns=list('abc'))
    >>> mdf
       a  b  c
    0  1  2  3
    >>> mdf.metadata
    {'constructor': {'class': metapandas.metadataframe.MetaDataFrame,
     'args': ([[1, 2, 3]],),
     'kwargs': {'columns': ['a', 'b', 'c']}}}
    """

    _metadata = ['metadata']  # lists properites which should be passed to copies

    def __init__(self, *args, **kwargs):
        """Wrap the pd.DataFrame.__init__ function.

        Notes
        -----
        The keyword argument :code:`metadata` can be used to
        initialise the MetaDataFrame.metadata dictionary.

        """
        metadata = kwargs.pop('metadata', {})
        super(MetaDataFrame, self).__init__(*args, **kwargs)
        metadata.update({
            'constructor': {
                'class': self.__class__,
                'args': args,
                'kwargs': kwargs
            }
        })
        self.metadata = metadata

    @property
    def _constructor(self):
        """Internal pandas property for extending DataFrame construction."""
        def wrapper(*args, **kwargs):
            df = MetaDataFrame(*args, **kwargs)
            # call custom methods here
            return df
        return wrapper
