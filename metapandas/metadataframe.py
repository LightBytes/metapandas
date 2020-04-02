import pandas as pd


class MetaDataFrame(pd.DataFrame):
    """A specialised DataFrame class for tracking metadata.
    
    Examples
    --------
    >>> from nats.utils.datasets.processing.metadata import MetaDataFrame
    >>> MetaDataFrame([1, 2, 3], columns='a')
    
    """
    _metadata = ['metadata']  # lists properites which should be passed to copies

    def __init__(self, *args, **kwargs):
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
        def wrapper(*args, **kwargs):
            df = MetaDataFrame(*args, **kwargs)
            # call custom methods here
            return df
        return wrapper