__author__ = 'Jernej Virag'

class AudioFormat(object):
    '''Audio details.

    An instance of this class is provided by sources with audio tracks.  You
    should not modify the fields, as they are used internally to describe the
    format of data provided by the source.

    :Ivariables:
        `channels` : int
            The number of channels: 1 for mono or 2 for stereo (pyglet does
            not yet support surround-sound sources).
        `sample_size` : int
            Bits per sample; only 8 or 16 are supported.
        `sample_rate` : int
            Samples per second (in Hertz).

    '''

    def __init__(self, channels, sample_size, sample_rate):
        self.channels = channels
        self.sample_size = sample_size
        self.sample_rate = sample_rate

        # Convenience
        self.bytes_per_sample = (sample_size >> 3) * channels
        self.bytes_per_second = self.bytes_per_sample * sample_rate

    def __eq__(self, other):
        return (self.channels == other.channels and
                self.sample_size == other.sample_size and
                self.sample_rate == other.sample_rate)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return '%s(channels=%d, sample_size=%d, sample_rate=%d)' % (
            self.__class__.__name__, self.channels, self.sample_size,
            self.sample_rate)
