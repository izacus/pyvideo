from ctypes import create_string_buffer, memmove
from exceptions import ImageException
import re

__author__ = 'Jernej Virag'

class VideoFormat(object):
    '''Video details.

    An instance of this class is provided by sources with a video track.  You
    should not modify the fields.

    Note that the sample aspect has no relation to the aspect ratio of the
    video image.  For example, a video image of 640x480 with sample aspect 2.0
    should be displayed at 1280x480.  It is the responsibility of the
    application to perform this scaling.

    :Ivariables:
        `width` : int
            Width of video image, in pixels.
        `height` : int
            Height of video image, in pixels.
        `sample_aspect` : float
            Aspect ratio (width over height) of a single video pixel.

    '''

    def __init__(self, width, height, sample_aspect=1.0):
        self.width = width
        self.height = height
        self.sample_aspect = sample_aspect

class ImageData(object):
    '''An image represented as a string of unsigned bytes.

    :Ivariables:
        `data` : str
            Pixel data, encoded according to `format` and `pitch`.
        `format` : str
            The format string to use when reading or writing `data`.
        `pitch` : int
            Number of bytes per row.  Negative values indicate a top-to-bottom
            arrangement.

    Setting the `format` and `pitch` instance variables and reading `data` is
    deprecated; use `get_data` and `set_data` in new applications.  (Reading
    `format` and `pitch` to obtain the current encoding is not deprecated).
    '''

    _swap1_pattern = re.compile('(.)', re.DOTALL)
    _swap2_pattern = re.compile('(.)(.)', re.DOTALL)
    _swap3_pattern = re.compile('(.)(.)(.)', re.DOTALL)
    _swap4_pattern = re.compile('(.)(.)(.)(.)', re.DOTALL)

    def __init__(self, width, height, format, data, pitch=None):
        '''Initialise image data.

        :Parameters:
            `width` : int
                Width of image data
            `height` : int
                Height of image data
            `format` : str
                A valid format string, such as 'RGB', 'RGBA', 'ARGB', etc.
            `data` : sequence
                String or array/list of bytes giving the decoded data.
            `pitch` : int or None
                If specified, the number of bytes per row.  Negative values
                indicate a top-to-bottom arrangement.  Defaults to
                ``width * len(format)``.

        '''
        self.width = width
        self.height = height

        self._current_format = format.upper()
        self._current_data = data
        if not pitch:
            pitch = width * len(format)
        self._current_pitch = self.pitch = pitch

    def get_data(self, format, pitch):
        '''Get the byte data of the image.

        :Parameters:
            `format` : str
                Format string of the return data.
            `pitch` : int
                Number of bytes per row.  Negative values indicate a
                top-to-bottom arrangement.

        :since: pyglet 1.1

        :rtype: sequence of bytes, or str
        '''
        if format == self._current_format and pitch == self._current_pitch:
            return self._current_data
        return self._convert(format, pitch)

    def set_data(self, format, pitch, data):
        '''Set the byte data of the image.

        :Parameters:
            `format` : str
                Format string of the return data.
            `pitch` : int
                Number of bytes per row.  Negative values indicate a
                top-to-bottom arrangement.
            `data` : str or sequence of bytes
                Image data.

        :since: pyglet 1.1
        '''
        self._current_format = format
        self._current_pitch = pitch
        self._current_data = data

    def _get_format(self):
        return self._current_format

    format = property(lambda self: self._get_format())

    def _get_pitch(self):
        return self._current_format

    def get_region(self, x, y, width, height):
        '''Retrieve a rectangular region of this image data.

        :Parameters:
            `x` : int
                Left edge of region.
            `y` : int
                Bottom edge of region.
            `width` : int
                Width of region.
            `height` : int
                Height of region.

        :rtype: ImageDataRegion
        '''
        return ImageDataRegion(x, y, width, height, self)

    def _get_data(self):
        if self._current_pitch != self.pitch or self._current_format != self.format:
            self._current_data = self._convert(self.format, self.pitch)
            self._current_format = self.format
            self._current_pitch = self.pitch

        self._ensure_string_data()
        return self._current_data

    def _set_data(self, data):
        self._current_data = data
        self._current_format = self.format
        self._current_pitch = self.pitch
        self._current_texture = None
        self._current_mipmapped_texture = None

    data = property(_get_data, _set_data,
        doc='''The byte data of the image.  Read-write.

        :deprecated: Use `get_data` and `set_data`.

        :type: sequence of bytes, or str
        ''')

    def _ensure_string_data(self):
        if type(self._current_data) is not str:
            buf = create_string_buffer(len(self._current_data))
            memmove(buf, self._current_data, len(self._current_data))
            self._current_data = buf.raw

    def _convert(self, format, pitch):
        '''Return data in the desired format; does not alter this instance's
        current format or pitch.
        '''
        if format == self._current_format and pitch == self._current_pitch:
            return self._current_data

        self._ensure_string_data()
        data = self._current_data
        current_pitch = self._current_pitch
        current_format = self._current_format
        sign_pitch = current_pitch / abs(current_pitch)
        if format != self._current_format:
            # Create replacement string, e.g. r'\4\1\2\3' to convert RGBA to
            # ARGB
            repl = ''
            for c in format:
                try:
                    idx = current_format.index(c) + 1
                except ValueError:
                    idx = 1
                repl += r'\%d' % idx

            if len(current_format) == 1:
                swap_pattern = self._swap1_pattern
            elif len(current_format) == 2:
                swap_pattern = self._swap2_pattern
            elif len(current_format) == 3:
                swap_pattern = self._swap3_pattern
            elif len(current_format) == 4:
                swap_pattern = self._swap4_pattern
            else:
                raise ImageException('Current image format is wider than 32 bits.')

            packed_pitch = self.width * len(current_format)
            if abs(self._current_pitch) != packed_pitch:
                # Pitch is wider than pixel data, need to go row-by-row.
                rows = re.findall('.' * abs(self._current_pitch), data, re.DOTALL)
                rows = [swap_pattern.sub(repl, r[:packed_pitch]) for r in rows]
                data = ''.join(rows)
            else:
                # Rows are tightly packed, apply regex over whole image.
                data = swap_pattern.sub(repl, data)

            # After conversion, rows will always be tightly packed
            current_pitch = sign_pitch * (len(format) * self.width)

        if pitch != current_pitch:
            diff = abs(current_pitch) - abs(pitch)
            if diff > 0:
                # New pitch is shorter than old pitch, chop bytes off each row
                pattern = re.compile(
                    '(%s)%s' % ('.' * abs(pitch), '.' * diff), re.DOTALL)
                data = pattern.sub(r'\1', data)
            elif diff < 0:
                # New pitch is longer than old pitch, add '0' bytes to each row
                pattern = re.compile(
                    '(%s)' % ('.' * abs(current_pitch)), re.DOTALL)
                pad = '.' * -diff
                data = pattern.sub(r'\1%s' % pad, data)

            if current_pitch * pitch < 0:
                # Pitch differs in sign, swap row order
                rows = re.findall('.' * abs(pitch), data, re.DOTALL)
                rows.reverse()
                data = ''.join(rows)

        return data

class ImageDataRegion(ImageData):
    def __init__(self, x, y, width, height, image_data):
        super(ImageDataRegion, self).__init__(width, height,
            image_data._current_format, image_data._current_data,
            image_data._current_pitch)
        self.x = x
        self.y = y

    def _get_data(self):
        # Crop the data first
        x1 = len(self._current_format) * self.x
        x2 = len(self._current_format) * (self.x + self.width)

        self._ensure_string_data()
        data = self._convert(self._current_format, abs(self._current_pitch))
        rows = re.findall('.' * abs(self._current_pitch), data, re.DOTALL)
        rows = [row[x1:x2] for row in rows[self.y:self.y+self.height]]
        self._current_data = ''.join(rows)
        self._current_pitch = self.width * len(self._current_format)
        self._current_texture = None
        self.x = 0
        self.y = 0

        return super(ImageDataRegion, self)._get_data()

    def _set_data(self, data):
        self.x = 0
        self.y = 0
        super(ImageDataRegion, self)._set_data(data)

    data = property(_get_data, _set_data)

    def get_data(self, format, pitch):
        x1 = len(self._current_format) * self.x
        x2 = len(self._current_format) * (self.x + self.width)

        self._ensure_string_data()
        data = self._convert(self._current_format, abs(self._current_pitch))
        rows = re.findall('.' * abs(self._current_pitch), data, re.DOTALL)
        rows = [row[x1:x2] for row in rows[self.y:self.y+self.height]]
        self._current_data = ''.join(rows)
        self._current_pitch = self.width * len(self._current_format)
        self._current_texture = None
        self.x = 0
        self.y = 0

        return super(ImageDataRegion, self).get_data(format, pitch)

    def _ensure_string_data(self):
        super(ImageDataRegion, self)._ensure_string_data()

    def get_region(self, x, y, width, height):
        x += self.x
        y += self.y
        return super(ImageDataRegion, self).get_region(x, y, width, height)