from collections import OrderedDict
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import IPython.html.widgets as ipywidgets

from .compatibility import add_class, remove_class


# Global variables to try and reduce overhead of loading the logo
MENPO_LOGO = None
MENPO_LOGO_SCALE = None


def _format_box(box, box_style, border_visible, border_color, border_style,
                border_width, padding, margin):
    r"""
    Function that defines the style of an IPython box.

    Parameters
    ----------
    box : `IPython.html.widgets.Box`, `IPython.html.widgets.FlexBox` or subclass
        The ipython box object.
    box_style : `str` or ``None`` (see below)
        Style options ::

            {``'success'``, ``'info'``, ``'warning'``, ``'danger'``, ``''``}
            or
            ``None``

    border_visible : `bool`
        Defines whether to draw the border line around the widget.
    border_color : `str`
        The color of the border around the widget.
    border_style : `str`
        The line style of the border around the widget.
    border_width : `float`
        The line width of the border around the widget.
    padding : `float`
        The padding around the widget.
    margin : `float`
        The margin around the widget.
    """
    box.box_style = box_style
    box.padding = padding
    box.margin = margin
    if border_visible:
        box.border_color = border_color
        box.border_style = border_style
        box.border_width = border_width
    else:
        box.border_width = 0


def _format_font(obj, font_family, font_size, font_style, font_weight):
    r"""
    Function that defines the font of a given IPython object.

    Parameters
    ----------
    obj : `IPython.html.widgets`
        The ipython widget object.
    font_family : See Below, optional
        The font of the axes.
        Example options ::

            {``serif``, ``sans-serif``, ``cursive``, ``fantasy``,
             ``monospace``}

    font_size : `int`, optional
        The font size of the axes.
    font_style : {``normal``, ``italic``, ``oblique``}, optional
        The font style of the axes.
    font_weight : See Below, optional
        The font weight of the axes.
        Example options ::

            {``ultralight``, ``light``, ``normal``, ``regular``,
             ``book``, ``medium``, ``roman``, ``semibold``,
             ``demibold``, ``demi``, ``bold``, ``heavy``,
             ``extra bold``, ``black``}
    """
    obj.font_family = font_family
    obj.font_size = font_size
    obj.font_style = font_style
    obj.font_weight = font_weight


class LogoWidget(ipywidgets.Box):
    r"""
    Creates a widget with Menpo's logo image. The widget consists of:

        1) Image [`self.image`]: the ipython image widget with Menpo's logo

    To set the styling of this widget please refer to the `style()` method.

    Parameters
    ----------
    scale : `float`, optional
        Defines the scale that will be applied to the logo image
        (`data/menpo_thumbnail.jpg`).
    """
    def __init__(self, scale=0.3):
        # Try to only load the logo once
        global MENPO_LOGO, MENPO_LOGO_SCALE
        if MENPO_LOGO is None or scale != MENPO_LOGO_SCALE:
            import menpo.io as mio
            image = mio.import_builtin_asset.menpo_thumbnail_jpg()
            MENPO_LOGO = image.rescale(scale)
            MENPO_LOGO_SCALE = scale

        self.image = ipywidgets.Image(value=_convert_image_to_bytes(MENPO_LOGO))
        super(LogoWidget, self).__init__(children=[self.image])

    def style(self, box_style=None, border_visible=True, border_color='black',
              border_style='solid', border_width=1, padding=0, margin=0):
        r"""
        Function that defines the styling of the widget.

        Parameters
        ----------
        box_style : `str` or ``None`` (see below), optional
            Style options ::

                {``'success'``, ``'info'``, ``'warning'``, ``'danger'``, ``''``}
                or
                ``None``

        border_visible : `bool`, optional
            Defines whether to draw the border line around the widget.
        border_color : `str`, optional
            The color of the border around the widget.
        border_style : `str`, optional
            The line style of the border around the widget.
        border_width : `float`, optional
            The line width of the border around the widget.
        padding : `float`, optional
            The padding around the widget.
        margin : `float`, optional
            The margin around the widget.
        """
        _format_box(self, box_style, border_visible, border_color, border_style,
                    border_width, padding, margin)


class IndexSliderWidget(ipywidgets.Box):
    r"""
    Creates a widget for selecting an index using a slider. The widget consists
    of:

        1) IntSlider [`self.slider`]: slider for selecting the index

    The selected values are stored in `self.selected_values` `dict`. To set the
    styling of this widget please refer to the `style()` method. To update the
    state and functions of the widget, please refer to the `set_widget_state()`,
    `set_update_function()` and `set_render_function()` methods.

    Parameters
    ----------
    index_default : `dict`
        The dictionary with the default options. For example ::

            index_default = {'min': 0, 'max': 100, 'step': 1, 'index': 10}

    render_function : `function` or ``None``, optional
        The render function that is executed when the index value changes.
        If ``None``, then nothing is assigned.
    update_function : `function` or ``None``, optional
        The update function that is executed when the index value changes.
        If ``None``, then nothing is assigned.
    description : `str`, optional
        The title of the widget.
    """
    def __init__(self, index_default, render_function=None,
                 update_function=None, description='Index: '):
        self.slider = ipywidgets.IntSlider(min=index_default['min'],
                                           max=index_default['max'],
                                           value=index_default['index'],
                                           step=index_default['step'],
                                           description=description)
        super(IndexSliderWidget, self).__init__(children=[self.slider])

        # Assign output
        self.selected_values = index_default

        # Set functionality
        def save_index(name, value):
            self.selected_values['index'] = value
        self.slider.on_trait_change(save_index, 'value')

        # Set render and update functions
        self._update_function = None
        self.add_update_function(update_function)
        self._render_function = None
        self.add_render_function(render_function)

    def style(self, box_style=None, border_visible=True, border_color='black',
              border_style='solid', border_width=1, padding=0, margin=0,
              font_family='', font_size=None, font_style='', font_weight=''):
        r"""
        Function that defines the styling of the widget.

        Parameters
        ----------
        box_style : `str` or ``None`` (see below), optional
            Style options ::

                {``'success'``, ``'info'``, ``'warning'``, ``'danger'``, ``''``}
                or
                ``None``

        border_visible : `bool`, optional
            Defines whether to draw the border line around the widget.
        border_color : `str`, optional
            The color of the border around the widget.
        border_style : `str`, optional
            The line style of the border around the widget.
        border_width : `float`, optional
            The line width of the border around the widget.
        padding : `float`, optional
            The padding around the widget.
        margin : `float`, optional
            The margin around the widget.
        font_family : See Below, optional
            The font family to be used.
            Example options ::

                {``'serif'``, ``'sans-serif'``, ``'cursive'``, ``'fantasy'``,
                 ``'monospace'``, ``'helvetica'``}

        font_size : `int`, optional
            The font size.
        font_style : {``'normal'``, ``'italic'``, ``'oblique'``}, optional
            The font style.
        font_weight : See Below, optional
            The font weight.
            Example options ::

                {``'ultralight'``, ``'light'``, ``'normal'``, ``'regular'``,
                 ``'book'``, ``'medium'``, ``'roman'``, ``'semibold'``,
                 ``'demibold'``, ``'demi'``, ``'bold'``, ``'heavy'``,
                 ``'extra bold'``, ``'black'``}
        """
        _format_box(self, box_style, border_visible, border_color, border_style,
                    border_width, padding, margin)
        _format_font(self, font_family, font_size, font_style,
                     font_weight)

    def add_render_function(self, render_function):
        r"""
        Method that adds a `render_function()` to the widget. The signature of
        the given function is also stored in `self._render_function`.

        Parameters
        ----------
        render_function : `function` or ``None``, optional
            The render function that behaves as a callback. If ``None``, then
            nothing is added.
        """
        self._render_function = render_function
        if self._render_function is not None:
            self.slider.on_trait_change(self._render_function, 'value')

    def remove_render_function(self):
        r"""
        Method that removes the current `self._render_function()` from the
        widget and sets ``self._render_function = None``.
        """
        self.slider.on_trait_change(self._render_function, 'value', remove=True)
        self._render_function = None

    def replace_render_function(self, render_function):
        r"""
        Method that replaces the current `self._render_function()` of the widget
        with the given `render_function()`.

        Parameters
        ----------
        render_function : `function` or ``None``, optional
            The render function that behaves as a callback. If ``None``, then
            nothing is happening.
        """
        # remove old function
        self.remove_render_function()

        # add new function
        self.add_render_function(render_function)

    def add_update_function(self, update_function):
        r"""
        Method that adds a `update_function()` to the widget. The signature of
        the given function is also stored in `self._update_function`.

        Parameters
        ----------
        update_function : `function` or ``None``, optional
            The update function that behaves as a callback. If ``None``, then
            nothing is added.
        """
        self._update_function = update_function
        if self._update_function is not None:
            self.slider.on_trait_change(self._update_function, 'value')

    def remove_update_function(self):
        r"""
        Method that removes the current `self._update_function()` from the
        widget and sets ``self._update_function = None``.
        """
        self.slider.on_trait_change(self._update_function, 'value', remove=True)
        self._update_function = None

    def replace_update_function(self, update_function):
        r"""
        Method that replaces the current `self._update_function()` of the widget
        with the given `update_function()`.

        Parameters
        ----------
        update_function : `function` or ``None``, optional
            The update function that behaves as a callback. If ``None``, then
            nothing is happening.
        """
        # remove old function
        self.remove_update_function()

        # add new function
        self.add_update_function(update_function)

    def set_widget_state(self, index_default, allow_callback=True):
        r"""
        Method that updates the state of the widget, if the provided
        `index_default` values are different than `self.selected_values()`.

        Parameter
        ---------
        index_default : `dict`
            The dictionary with the selected options. For example ::

                index_default = {'min': 0, 'max': 100, 'step': 1, 'index': 10}
        allow_callback : `bool`, optional
            If ``True``, it allows triggering of any callback functions.
        """
        # Check if update is required
        if not (index_default['min'] == self.selected_values['min'] and
                index_default['max'] == self.selected_values['max'] and
                index_default['step'] == self.selected_values['step'] and
                index_default['index'] == self.selected_values['index']):
            if not allow_callback:
                # temporarily remove render and update functions
                render_function = self._render_function
                update_function = self._update_function
                self.remove_render_function()
                self.remove_update_function()

            # set values to slider
            self.slider.min = index_default['min']
            self.slider.max = index_default['max']
            self.slider.step = index_default['step']
            self.slider.value = index_default['index']

            if not allow_callback:
                # re-assign render and update callbacks
                self.add_update_function(update_function)
                self.add_render_function(render_function)

        # Assign output
        self.selected_values = index_default


class IndexButtonsWidget(ipywidgets.FlexBox):
    r"""
    Creates a widget for selecting an index using plus/minus buttons. The widget
    consists of:

        1) Latex [`self.title`]: the description of the widget
        2) Button [`self.button_plus`]: the plus button to increase the index
        3) Button [`self.button_minus`]: the minus button to decrease the index
        4) IntText [`self.index_text`]: text area with the selected index. It
           can either be editable or not.

    The selected values are stored in `self.selected_values` `dict`. To set the
    styling of this widget please refer to the `style()` method. To update the
    state and functions of the widget, please refer to the `set_widget_state()`,
    `set_update_function()` and `set_render_function()` methods.

    Parameters
    ----------
    index_default : `dict`
        The dictionary with the default options. For example ::

            index_default = {'min': 0, 'max': 100, 'step': 1, 'index': 10}

    render_function : `function` or ``None``, optional
        The render function that is executed when the index value changes.
        If ``None``, then nothing is assigned.
    update_function : `function` or ``None``, optional
        The update function that is executed when the index value changes.
        If ``None``, then nothing is assigned.
    description : `str`, optional
        The title of the widget.
    minus_description : `str`, optional
        The title of the button that decreases the index.
    plus_description : `str`, optional
        The title of the button that increases the index.
    loop : `bool`, optional
        If ``True``, then if by pressing the buttons we reach the minimum
        (maximum) index values, then the counting will continue from the end
        (beginning). If ``False``, the counting will stop at the minimum
        (maximum) value.
    text_editable : `bool`, optional
        Flag that determines whether the index text will be editable.
    """
    def __init__(self, index_default, render_function=None,
                 update_function=None, description='Index: ',
                 minus_description='-', plus_description='+', loop_enabled=True,
                 text_editable=True):
        self.title = ipywidgets.Latex(value=description)
        self.button_minus = ipywidgets.Button(description=minus_description)
        self.button_plus = ipywidgets.Button(description=plus_description)
        self.index_text = ipywidgets.IntText(value=index_default['index'],
                                             min=index_default['min'],
                                             max=index_default['max'],
                                             disabled=not text_editable)
        super(IndexButtonsWidget, self).__init__(children=[self.title,
                                                           self.button_minus,
                                                           self.index_text,
                                                           self.button_plus])
        self.loop_enabled = loop_enabled
        self.text_editable = text_editable

        # Align
        self.orientation = 'horizontal'
        self.align = 'center'

        # Assign output
        self.selected_values = index_default

        # Set functionality
        def value_plus(name):
            tmp_val = int(self.index_text.value) + self.selected_values['step']
            if tmp_val > self.selected_values['max']:
                if self.loop_enabled:
                    self.index_text.value = str(self.selected_values['min'])
                else:
                    self.index_text.value = str(self.selected_values['max'])
            else:
                self.index_text.value = str(tmp_val)
        self.button_plus.on_click(value_plus)

        def value_minus(name):
            tmp_val = int(self.index_text.value) - self.selected_values['step']
            if tmp_val < self.selected_values['min']:
                if self.loop_enabled:
                    self.index_text.value = str(self.selected_values['max'])
                else:
                    self.index_text.value = str(self.selected_values['min'])
            else:
                self.index_text.value = str(tmp_val)
        self.button_minus.on_click(value_minus)

        def save_index(name, value):
            self.selected_values['index'] = int(value)
        self.index_text.on_trait_change(save_index, 'value')

        # Set render and update functions
        self._update_function = None
        self.add_update_function(update_function)
        self._render_function = None
        self.add_render_function(render_function)

    def style(self, box_style=None, border_visible=True, border_color='black',
              border_style='solid', border_width=1, padding=0, margin=0,
              font_family='', font_size=None, font_style='', font_weight='',
              buttons_width='1cm', text_width='4cm', title_padding=6):
        r"""
        Function that defines the styling of the widget.

        Parameters
        ----------
        box_style : `str` or ``None`` (see below), optional
            Style options ::

                {``'success'``, ``'info'``, ``'warning'``, ``'danger'``, ``''``}
                or
                ``None``

        border_visible : `bool`, optional
            Defines whether to draw the border line around the widget.
        border_color : `str`, optional
            The color of the border around the widget.
        border_style : `str`, optional
            The line style of the border around the widget.
        border_width : `float`, optional
            The line width of the border around the widget.
        padding : `float`, optional
            The padding around the widget.
        margin : `float`, optional
            The margin around the widget.
        font_family : See Below, optional
            The font family to be used.
            Example options ::

                {``'serif'``, ``'sans-serif'``, ``'cursive'``, ``'fantasy'``,
                 ``'monospace'``, ``'helvetica'``}

        font_size : `int`, optional
            The font size.
        font_style : {``'normal'``, ``'italic'``, ``'oblique'``}, optional
            The font style.
        font_weight : See Below, optional
            The font weight.
            Example options ::

                {``'ultralight'``, ``'light'``, ``'normal'``, ``'regular'``,
                 ``'book'``, ``'medium'``, ``'roman'``, ``'semibold'``,
                 ``'demibold'``, ``'demi'``, ``'bold'``, ``'heavy'``,
                 ``'extra bold'``, ``'black'``}

        buttons_width : `str`, optional
            The width of the buttons.
        text_width : `str`, optional
            The width of the index text area.
        title_padding : `float`, optional
            The padding around the title (description) text.
        """
        _format_box(self, box_style, border_visible, border_color, border_style,
                    border_width, padding, margin)
        # TODO: How to change the width of a *Text widget?
        #self.index_text.width = text_width
        self.button_minus.width = buttons_width
        self.button_plus.width = buttons_width
        self.title.padding = title_padding
        _format_font(self.title, font_family, font_size, font_style,
                     font_weight)
        _format_font(self.button_minus, font_family, font_size, font_style,
                     font_weight)
        _format_font(self.button_plus, font_family, font_size, font_style,
                     font_weight)
        _format_font(self.index_text, font_family, font_size, font_style,
                     font_weight)

    def add_render_function(self, render_function):
        r"""
        Method that adds a `render_function()` to the widget. The signature of
        the given function is also stored in `self._render_function`.

        Parameters
        ----------
        render_function : `function` or ``None``, optional
            The render function that behaves as a callback. If ``None``, then
            nothing is added.
        """
        self._render_function = render_function
        if self._render_function is not None:
            self.index_text.on_trait_change(self._render_function, 'value')

    def remove_render_function(self):
        r"""
        Method that removes the current `self._render_function()` from the
        widget and sets ``self._render_function = None``.
        """
        self.index_text.on_trait_change(self._render_function, 'value',
                                        remove=True)
        self._render_function = None

    def replace_render_function(self, render_function):
        r"""
        Method that replaces the current `self._render_function()` of the widget
        with the given `render_function()`.

        Parameters
        ----------
        render_function : `function` or ``None``, optional
            The render function that behaves as a callback. If ``None``, then
            nothing is happening.
        """
        # remove old function
        self.remove_render_function()

        # add new function
        self.add_render_function(render_function)

    def add_update_function(self, update_function):
        r"""
        Method that adds a `update_function()` to the widget. The signature of
        the given function is also stored in `self._update_function`.

        Parameters
        ----------
        update_function : `function` or ``None``, optional
            The update function that behaves as a callback. If ``None``, then
            nothing is added.
        """
        self._update_function = update_function
        if self._update_function is not None:
            self.index_text.on_trait_change(self._update_function, 'value')

    def remove_update_function(self):
        r"""
        Method that removes the current `self._update_function()` from the
        widget and sets ``self._update_function = None``.
        """
        self.index_text.on_trait_change(self._update_function, 'value',
                                        remove=True)
        self._update_function = None

    def replace_update_function(self, update_function):
        r"""
        Method that replaces the current `self._update_function()` of the widget
        with the given `update_function()`.

        Parameters
        ----------
        update_function : `function` or ``None``, optional
            The update function that behaves as a callback. If ``None``, then
            nothing is happening.
        """
        # remove old function
        self.remove_update_function()

        # add new function
        self.add_update_function(update_function)

    def set_widget_state(self, index_default, loop_enabled, text_editable,
                         allow_callback=True):
        r"""
        Method that updates the state of the widget, if the provided
        `index_default` values are different than `self.selected_values()`.

        Parameter
        ---------
        index_default : `dict`
            The dictionary with the selected options. For example ::

                index_default = {'min': 0, 'max': 100, 'step': 1, 'index': 10}
        allow_callback : `bool`, optional
            If ``True``, it allows triggering of any callback functions.
        """
        # Update loop_enabled and text_editable
        self.loop_enabled = loop_enabled
        self.text_editable = text_editable
        self.index_text.disabled = not text_editable

        # Check if update is required
        if not index_default['index'] == self.selected_values['index']:
            if not allow_callback:
                # temporarily remove render and update functions
                render_function = self._render_function
                update_function = self._update_function
                self.remove_render_function()
                self.remove_update_function()

            # set value to index text
            self.index_text.value = str(index_default['index'])

            if not allow_callback:
                # re-assign render and update callbacks
                self.add_update_function(update_function)
                self.add_render_function(render_function)

        # Assign output
        self.selected_values = index_default


def _decode_colour(colour):
    r"""
    Function that decodes a given colour to its RGB values.

    Parameters
    ----------
    obj : `str` or `list`
        Either an `str` colour or a `list` of length ``3`` with the RGB values.

    Returns
    -------
    colour : `str`
        Returns either the original `colour` of ``'custom'`` if the original
        `colour` was a `list`.
    r_val : `float`
        The R channel. ``0.`` if `colour` is an `str`.
    g_val : `float`
        The G channel. ``0.`` if `colour` is an `str`.
    b_val : `float`
        The B channel. ``0.`` if `colour` is an `str`.
    """
    r_val = g_val = b_val = 0.
    if not isinstance(colour, str):
        r_val = colour[0]
        g_val = colour[1]
        b_val = colour[2]
        colour = 'custom'
    return colour, r_val, g_val, b_val


def _lists_are_the_same(a, b):
    r"""
    Function that checks if two `lists` have the same elements in the same
    order.

    Returns
    -------
    _lists_are_the_same : `bool`
        ``True`` if the lists are the same.
    """
    if len(a) == len(b):
        for i, j in zip(a, b):
            if i != j:
                return False
        return True
    else:
        return False


class ColourSelectionWidget(ipywidgets.FlexBox):
    r"""
    Creates a widget for colour selection of various items. The widget consists
    of:

        1) Dropdown [`self.label_dropdown`]: the menu with the available labels
        2) Button [`self.apply_to_all_button`]: button that sets the same colour
           to all available labels
        3) VBox [`self.labels_box`]: the box containing (1) and (2)
        4) Dropdown [`self.colour_dropdown`]: the menu with the predefined
           colours and custom option
        5) BoundedFloatText [`self.r_text`]: text area for the R value
        6) BoundedFloatText [`self.g_text`]: text area for the G value
        7) BoundedFloatText [`self.b_text`]: text area for the B value
        8) Box [`self.rgb_box`]: box with (5), (6) and (7)

    The selected values are stored in `self.selected_values` `dict`. To set the
    styling of this widget please refer to the `style()` method. To update the
    state and function of the widget, please refer to the `set_widget_state()`
    and `set_render_function()` methods.

    Parameters
    ----------
    colours_list : `list` of `str` or [`float`, `float`, `float`]
        If `str`, it must be one of ::

            {``'b'``, ``'g'``, ``'r'``, ``'c'``,
             ``'m'``, ``'y'``, ``'k'``, ``'w'``}

        If [`float`, `float`, `float`], it defines an RGB value and must have
        length 3.
    render_function : `function` or ``None``, optional
        The render function that is executed when a widgets' value changes.
        If ``None``, then nothing is assigned.
    description : `str`, optional
        The description of the widget.
    labels : `list` or ``None``, optional
        A `list` with the labels' names. If ``None``, then a `list` of the form
        ``label {}`` is automatically defined.
    """
    def __init__(self, colours_list, render_function=None, description='Colour',
                 labels=None):
        # Check if multiple mode should be enabled
        n_labels = len(colours_list)
        multiple = n_labels > 1

        # Colours dictionary
        colour_dict = OrderedDict()
        colour_dict['blue'] = 'b'
        colour_dict['green'] = 'g'
        colour_dict['red'] = 'r'
        colour_dict['cyan'] = 'c'
        colour_dict['magenta'] = 'm'
        colour_dict['yellow'] = 'y'
        colour_dict['black'] = 'k'
        colour_dict['white'] = 'w'
        colour_dict['custom'] = 'custom'

        # Labels dropdown menu (it must be invisible if multiple == False)
        labels_dict = OrderedDict()
        if labels is None:
            labels = []
            for k in range(n_labels):
                labels_dict["label {}".format(k)] = k
                labels.append("label {}".format(k))
        else:
            for k, l in enumerate(labels):
                labels_dict[l] = k
        self.label_dropdown = ipywidgets.Dropdown(options=labels_dict, value=0)
        self.apply_to_all_button = ipywidgets.Button(
            description='apply to all labels')
        self.labels_box = ipywidgets.VBox(children=[self.label_dropdown,
                                                    self.apply_to_all_button],
                                          visible=multiple, align='end')

        # Decode colour values of the first label
        default_colour, r_val, g_val, b_val = _decode_colour(colours_list[0])

        # Create colour widgets
        self.r_text = ipywidgets.BoundedFloatText(value=r_val, min=0.0, max=1.0,
                                                  description='R')
        self.g_text = ipywidgets.BoundedFloatText(value=g_val, min=0.0, max=1.0,
                                                  description='G')
        self.b_text = ipywidgets.BoundedFloatText(value=b_val, min=0.0, max=1.0,
                                                  description='B')
        self.colour_dropdown = ipywidgets.Dropdown(options=colour_dict,
                                                   value=default_colour,
                                                   description='')
        self.rgb_box = ipywidgets.Box(children=[self.r_text, self.g_text,
                                                self.b_text],
                                      visible=default_colour == 'custom')

        # Set widget description
        if multiple:
            self.label_dropdown.description = description
        else:
            self.colour_dropdown.description = description

        # Final widget
        super(ColourSelectionWidget, self).__init__(
            children=[self.labels_box, self.colour_dropdown, self.rgb_box])
        self.align = 'end'

        # Assign output
        self.selected_values = {'colour': colours_list, 'labels': labels}

        # Set functionality
        def show_rgb_box(name, value):
            self.rgb_box.visible = value == 'custom'
        self.colour_dropdown.on_trait_change(show_rgb_box, 'value')

        def apply_to_all_function(name):
            if self.colour_dropdown.value == 'custom':
                tmp = [self.r_text.value, self.g_text.value, self.b_text.value]
            else:
                tmp = self.colour_dropdown.value
            for idx in range(len(self.selected_values['colour'])):
                self.selected_values['colour'][idx] = tmp
            self.label_dropdown.value = 0
        self.apply_to_all_button.on_click(apply_to_all_function)

        def update_colour_wrt_label(name, value):
            # temporarily remove render_function from r, g, b traits
            self.colour_dropdown._remove_notifiers(self._render_function, 'value')
            self.r_text._remove_notifiers(self._render_function, 'value')
            self.g_text._remove_notifiers(self._render_function, 'value')
            self.b_text._remove_notifiers(self._render_function, 'value')
            # update colour widgets
            (self.colour_dropdown.value, self.r_text.value, self.g_text.value,
             self.b_text.value) = _decode_colour(
                self.selected_values['colour'][value])
            # re-assign render_function
            self.colour_dropdown._add_notifiers(self._render_function, 'value')
            self.r_text._add_notifiers(self._render_function, 'value')
            self.g_text._add_notifiers(self._render_function, 'value')
            self.b_text._add_notifiers(self._render_function, 'value')
        self.label_dropdown.on_trait_change(update_colour_wrt_label, 'value')

        def save_colour(name, value):
            idx = self.label_dropdown.value
            if self.colour_dropdown.value == 'custom':
                self.selected_values['colour'][idx] = [self.r_text.value,
                                                       self.g_text.value,
                                                       self.b_text.value]
            else:
                self.selected_values['colour'][idx] = self.colour_dropdown.value
        self.colour_dropdown.on_trait_change(save_colour, 'value')
        self.r_text.on_trait_change(save_colour, 'value')
        self.g_text.on_trait_change(save_colour, 'value')
        self.b_text.on_trait_change(save_colour, 'value')

        # Set render function
        self._render_function = None
        self._apply_to_all_render_function = None
        self.add_render_function(render_function)

    def style(self, box_style=None, border_visible=True, border_color='black',
              border_style='solid', border_width=1, padding=0, margin=0,
              font_family='', font_size=None, font_style='',
              font_weight='', rgb_width='0.5cm'):
        r"""
        Function that defines the styling of the widget.

        Parameters
        ----------
        box_style : `str` or ``None`` (see below), optional
            Style options ::

                {``'success'``, ``'info'``, ``'warning'``, ``'danger'``, ``''``}
                or
                ``None``

        border_visible : `bool`, optional
            Defines whether to draw the border line around the widget.
        border_color : `str`, optional
            The color of the border around the widget.
        border_style : `str`, optional
            The line style of the border around the widget.
        border_width : `float`, optional
            The line width of the border around the widget.
        padding : `float`, optional
            The padding around the widget.
        margin : `float`, optional
            The margin around the widget.
        font_family : See Below, optional
            The font family to be used.
            Example options ::

                {``'serif'``, ``'sans-serif'``, ``'cursive'``, ``'fantasy'``,
                 ``'monospace'``, ``'helvetica'``}

        font_size : `int`, optional
            The font size.
        font_style : {``'normal'``, ``'italic'``, ``'oblique'``}, optional
            The font style.
        font_weight : See Below, optional
            The font weight.
            Example options ::

                {``'ultralight'``, ``'light'``, ``'normal'``, ``'regular'``,
                 ``'book'``, ``'medium'``, ``'roman'``, ``'semibold'``,
                 ``'demibold'``, ``'demi'``, ``'bold'``, ``'heavy'``,
                 ``'extra bold'``, ``'black'``}

        rgb_width : `str`, optional
            The width of the RGB texts.
        """
        _format_box(self, box_style, border_visible, border_color, border_style,
                    border_width, padding, margin)
        # TODO: How to change the width of a *Text widget?
        #self.r_text.width = rgb_width
        #self.g_text.width = rgb_width
        #self.b_text.width = rgb_width
        _format_font(self, font_family, font_size, font_style, font_weight)
        _format_font(self.label_dropdown, font_family, font_size, font_style,
                     font_weight)
        _format_font(self.apply_to_all_button, font_family, font_size,
                     font_style, font_weight)
        _format_font(self.r_text, font_family, font_size, font_style,
                     font_weight)
        _format_font(self.g_text, font_family, font_size, font_style,
                     font_weight)
        _format_font(self.b_text, font_family, font_size, font_style,
                     font_weight)
        _format_font(self.colour_dropdown, font_family, font_size, font_style,
                     font_weight)

    def add_render_function(self, render_function):
        r"""
        Method that adds a `render_function()` to the widget. The signature of
        the given function is also stored in `self._render_function`.

        Parameters
        ----------
        render_function : `function` or ``None``, optional
            The render function that behaves as a callback. If ``None``, then
            nothing is added.
        """
        self._render_function = render_function
        self._apply_to_all_render_function = None
        if self._render_function is not None:
            self.colour_dropdown.on_trait_change(self._render_function, 'value')
            self.r_text.on_trait_change(self._render_function, 'value')
            self.g_text.on_trait_change(self._render_function, 'value')
            self.b_text.on_trait_change(self._render_function, 'value')

            def apply_to_all_render_function(name):
                self._render_function('', True)
            self._apply_to_all_render_function = apply_to_all_render_function
            self.apply_to_all_button.on_click(
                self._apply_to_all_render_function)

    def remove_render_function(self):
        r"""
        Method that removes the current `self._render_function()` from the
        widget and sets ``self._render_function = None``.
        """
        self.colour_dropdown.on_trait_change(self._render_function, 'value',
                                             remove=True)
        self.r_text.on_trait_change(self._render_function, 'value', remove=True)
        self.g_text.on_trait_change(self._render_function, 'value', remove=True)
        self.b_text.on_trait_change(self._render_function, 'value', remove=True)
        self.apply_to_all_button.on_click(self._apply_to_all_render_function,
                                          remove=True)
        self._render_function = None
        self._apply_to_all_render_function = None

    def replace_render_function(self, render_function):
        r"""
        Method that replaces the current `self._render_function()` of the widget
        with the given `render_function()`.

        Parameters
        ----------
        render_function : `function` or ``None``, optional
            The render function that behaves as a callback. If ``None``, then
            nothing is happening.
        """
        # remove old function
        self.remove_render_function()

        # add new function
        self.add_render_function(render_function)

    def set_widget_state(self, colours_list, labels=None, allow_callback=True):
        r"""
        Method that updates the state of the widget, if the provided
        `colours_list` and `labels` values are different than
        `self.selected_values()`.

        Parameter
        ---------
        colours_list : `list` of `str` or [`float`, `float`, `float`]
            If `str`, it must be one of ::

                {``'b'``, ``'g'``, ``'r'``, ``'c'``,
                 ``'m'``, ``'y'``, ``'k'``, ``'w'``}

            If [`float`, `float`, `float`], it defines an RGB value and must
            have length 3.
        labels : `list` or ``None``, optional
            A `list` with the labels' names. If ``None``, then a `list` of the
            form ``label {}`` is automatically defined.
        allow_callback : `bool`, optional
            If ``True``, it allows triggering of any callback functions.
        """
        if labels is None:
            labels = self.selected_values['labels']

        sel_colours = self.selected_values['colour']
        sel_labels = self.selected_values['labels']
        if (_lists_are_the_same(sel_colours, colours_list) and
                not _lists_are_the_same(sel_labels, labels)):
            # the provided colours are the same, but the labels changed, so
            # update the labels
            self.selected_values['labels'] = labels
            labels_dict = OrderedDict()
            for k, l in enumerate(labels):
                labels_dict[l] = k
            self.label_dropdown.options = labels_dict
            if len(labels) > 1:
                if self.label_dropdown.value > 0:
                    self.label_dropdown.value = 0
                else:
                    self.label_dropdown.value = 1
                    self.label_dropdown.value = 0
        elif (not _lists_are_the_same(sel_colours, colours_list) and
              _lists_are_the_same(sel_labels, labels)):
            # the provided labels are the same, but the colours are different
            # assign colour
            self.selected_values['colour'] = colours_list
            # temporarily remove render_function from r, g, b traits
            render_function = self._render_function
            self.remove_render_function()
            # update colour widgets
            k = self.label_dropdown.value
            (self.colour_dropdown.value, self.r_text.value, self.g_text.value,
             self.b_text.value) = _decode_colour(colours_list[k])
            # re-assign render_function
            self.add_render_function(render_function)
            # trigger render function if allowed
            if allow_callback:
                self._render_function('', True)
        elif (not _lists_are_the_same(sel_colours, colours_list) and
              not _lists_are_the_same(sel_labels, labels)):
            # both the colours and the labels are different
            if len(sel_labels) > 1 and len(labels) == 1:
                self.colour_dropdown.description = \
                    self.label_dropdown.description
                self.label_dropdown.description = ''
            elif len(sel_labels) == 1 and len(labels) > 1:
                self.label_dropdown.description = \
                    self.colour_dropdown.description
                self.colour_dropdown.description = ''
            self.labels_box.visible = len(labels) > 1
            self.selected_values['colour'] = colours_list
            self.selected_values['labels'] = labels
            labels_dict = OrderedDict()
            for k, l in enumerate(labels):
                labels_dict[l] = k
            self.label_dropdown.options = labels_dict
            self.label_dropdown.value = 0
            # temporarily remove render_function from r, g, b traits
            render_function = self._render_function
            self.remove_render_function()
            # update colour widgets
            (self.colour_dropdown.value, self.r_text.value, self.g_text.value,
             self.b_text.value) = _decode_colour(colours_list[0])
            # re-assign render_function
            self.add_render_function(render_function)
            # trigger render function if allowed
            if allow_callback:
                self._render_function('', True)

    def disabled(self, disabled):
        r"""
        Method that disables the widget, if the ``disabled == True``.

        Parameter
        ---------
        disabled : `bool`
            If ``True``, the widget is disabled.
        """
        self.label_dropdown.disabled = disabled
        self.apply_to_all_button.disabled = disabled
        self.colour_dropdown.disabled = disabled
        self.r_text.disabled = disabled
        self.b_text.disabled = disabled
        self.g_text.disabled = disabled


class ImageOptionsWidget(ipywidgets.Box):
    r"""
    Creates a widget for selecting image rendering options. Specifically, it
    consists of:

        1) ToggleButton [`self.toggle_visible`]: toggle buttons that controls
           the options' visibility
        2) Checkbox [`self.interpolation_checkbox`]: interpolation checkbox
        3) FloatSlider [`self.alpha_slider`]: sets the alpha value
        4) Box [`self.options_box`]: box that contains (2) and (3)

    The selected values are stored in `self.selected_values` `dict`. To set the
    styling of this widget please refer to the `style()` method. To update the
    state and function of the widget, please refer to the `set_widget_state()`
    and `set_render_function()` methods.

    Parameters
    ----------
    image_options_default : `dict`
        The initial image options. Example ::

            image_options_default = {'alpha': 1., 'interpolation': 'bilinear'}

    render_function : `function` or ``None``, optional
        The render function that is executed when a widgets' value changes.
        If ``None``, then nothing is assigned.
    toggle_show_default : `bool`, optional
        Defines whether the options will be visible upon construction.
    toggle_show_visible : `bool`, optional
        The visibility of the toggle button.
    toggle_title : `str`, optional
        The title of the toggle button.
    """
    def __init__(self, image_options_default, render_function=None,
                 toggle_show_visible=True, toggle_show_default=True,
                 toggle_title='Image Object'):
        self.toggle_visible = ipywidgets.ToggleButton(
            description=toggle_title, value=toggle_show_default,
            visible=toggle_show_visible)
        self.interpolation_checkbox = ipywidgets.Checkbox(
            description='Pixelated',
            value=image_options_default['interpolation'] == 'none')
        self.alpha_slider = ipywidgets.FloatSlider(
            description='Alpha', value=image_options_default['alpha'],
            min=0.0, max=1.0, step=0.05)
        self.options_box = ipywidgets.Box(children=[self.interpolation_checkbox,
                                                    self.alpha_slider],
                                          visible=toggle_show_default)
        super(ImageOptionsWidget, self).__init__(children=[self.toggle_visible,
                                                           self.options_box])

        # Assign output
        self.selected_values = image_options_default

        # Set functionality
        def save_interpolation(name, value):
            if value:
                self.selected_values['interpolation'] = 'none'
            else:
                self.selected_values['interpolation'] = 'bilinear'
        self.interpolation_checkbox.on_trait_change(save_interpolation, 'value')

        def save_alpha(name, value):
            self.selected_values['alpha'] = value
        self.alpha_slider.on_trait_change(save_alpha, 'value')

        def toggle_function(name, value):
            self.options_box.visible = value
        self.toggle_visible.on_trait_change(toggle_function, 'value')

        # Set render function
        self._render_function = None
        self.add_render_function(render_function)

    def style(self, box_style=None, border_visible=False, border_color='black',
              border_style='solid', border_width=1, padding=0, margin=0,
              font_family='', font_size=None, font_style='',
              font_weight='', slider_width=''):
        r"""
        Function that defines the styling of the widget.

        Parameters
        ----------
        box_style : `str` or ``None`` (see below), optional
            Widget style options ::

                {``'success'``, ``'info'``, ``'warning'``, ``'danger'``, ``''``}
                or
                ``None``

        border_visible : `bool`, optional
            Defines whether to draw the border line around the widget.
        border_color : `str`, optional
            The color of the border around the widget.
        border_style : `str`, optional
            The line style of the border around the widget.
        border_width : `float`, optional
            The line width of the border around the widget.
        padding : `float`, optional
            The padding around the widget.
        margin : `float`, optional
            The margin around the widget.
        font_family : See Below, optional
            The font family to be used.
            Example options ::

                {``'serif'``, ``'sans-serif'``, ``'cursive'``, ``'fantasy'``,
                 ``'monospace'``, ``'helvetica'``}

        font_size : `int`, optional
            The font size.
        font_style : {``'normal'``, ``'italic'``, ``'oblique'``}, optional
            The font style.
        font_weight : See Below, optional
            The font weight.
            Example options ::

                {``'ultralight'``, ``'light'``, ``'normal'``, ``'regular'``,
                 ``'book'``, ``'medium'``, ``'roman'``, ``'semibold'``,
                 ``'demibold'``, ``'demi'``, ``'bold'``, ``'heavy'``,
                 ``'extra bold'``, ``'black'``}

        slider_width : `str`, optional
            The width of the slider.
        """
        _format_box(self, box_style, border_visible, border_color, border_style,
                    border_width, padding, margin)
        self.alpha_slider.width = slider_width
        _format_font(self, font_family, font_size, font_style, font_weight)
        _format_font(self.alpha_slider, font_family, font_size, font_style,
                     font_weight)
        _format_font(self.interpolation_checkbox, font_family, font_size,
                     font_style, font_weight)
        _format_font(self.toggle_visible, font_family, font_size, font_style,
                     font_weight)

    def add_render_function(self, render_function):
        r"""
        Method that adds a `render_function()` to the widget. The signature of
        the given function is also stored in `self._render_function`.

        Parameters
        ----------
        render_function : `function` or ``None``, optional
            The render function that behaves as a callback. If ``None``, then
            nothing is added.
        """
        self._render_function = render_function
        if self._render_function is not None:
            self.interpolation_checkbox.on_trait_change(self._render_function,
                                                        'value')
            self.alpha_slider.on_trait_change(self._render_function, 'value')

    def remove_render_function(self):
        r"""
        Method that removes the current `self._render_function()` from the
        widget and sets ``self._render_function = None``.
        """
        self.interpolation_checkbox.on_trait_change(self._render_function,
                                                    'value', remove=True)
        self.alpha_slider.on_trait_change(self._render_function, 'value',
                                          remove=True)
        self._render_function = None

    def replace_render_function(self, render_function):
        r"""
        Method that replaces the current `self._render_function()` of the widget
        with the given `render_function()`.

        Parameters
        ----------
        render_function : `function` or ``None``, optional
            The render function that behaves as a callback. If ``None``, then
            nothing is happening.
        """
        # remove old function
        self.remove_render_function()

        # add new function
        self.add_render_function(render_function)

    def set_widget_state(self, image_options_dict, allow_callback=True):
        r"""
        Method that updates the state of the widget, if the provided
        `image_options_dict` is different than `self.selected_values()`.

        Parameter
        ---------
        image_options_dict : `dict`
            The image options. Example ::

                image_options_default = {'alpha': 1.,
                                         'interpolation': 'bilinear'}
        allow_callback : `bool`, optional
            If ``True``, it allows triggering of any callback functions.
        """
        # Assign new options dict to selected_values
        self.selected_values = image_options_dict

        # temporarily remove render callback
        render_function = self._render_function
        self.remove_render_function()

        # update alpha slider
        if 'alpha' in image_options_dict.keys():
            self.alpha_slider.value = image_options_dict['alpha']

        # update interpolation checkbox
        if 'interpolation' in image_options_dict.keys():
            self.interpolation_checkbox.value = \
                image_options_dict['interpolation'] == 'none'

        # re-assign render callback
        self.add_render_function(render_function)

        # trigger render function if allowed
        if allow_callback:
            self._render_function('', True)


class LineOptionsWidget(ipywidgets.Box):
    r"""
    Creates a widget for selecting line rendering options. Specifically, it
    consists of:

        1) ToggleButton [`self.toggle_visible`]: toggle buttons that controls
           the options' visibility
        2) Checkbox [`self.render_lines_checkbox`]: whether to render lines
        3) BoundedFloatText [`self.line_width_text`]: sets the line width
        4) Dropdown [`self.line_style_dropdown`]: sets the line style
        5) ColourSelectionWidget [`self.line_colour_widget`]: sets line colour
        6) Box [`self.line_options_box`]: box that contains (3), (4) and (5)
        7) Box [`self.options_box`]: box that contains (2) and (6)

    The selected values are stored in `self.selected_values` `dict`. To set the
    styling of this widget please refer to the `style()` method. To update the
    state and function of the widget, please refer to the `set_widget_state()`
    and `set_render_function()` methods.

    Parameters
    ----------
    line_options_default : `dict`
        The initial line options. Example ::

            line_options_default = {'render_lines': True,
                                    'line_width': 1,
                                    'line_colour': ['b'],
                                    'line_style': '-'}

    render_function : `function` or ``None``, optional
        The render function that is executed when a widgets' value changes.
        If ``None``, then nothing is assigned.
    toggle_show_default : `bool`, optional
        Defines whether the options will be visible upon construction.
    toggle_show_visible : `bool`, optional
        The visibility of the toggle button.
    toggle_title : `str`, optional
        The title of the toggle button.
    render_checkbox_title : `str`, optional
        The description of the show line checkbox.
    labels : `list` or ``None``, optional
        A `list` with the labels' names that get passed in to the
        `ColourSelectionWidget`. If ``None``, then a `list` of the form
        ``label {}`` is automatically defined. Note that the labels are defined
        only for the colour option and not the rest of the options.
    """
    def __init__(self, line_options_default, render_function=None,
                 toggle_show_visible=True, toggle_show_default=True,
                 toggle_title='Line Object',
                 render_checkbox_title='Render lines', labels=None):
        self.toggle_visible = ipywidgets.ToggleButton(
            description=toggle_title, value=toggle_show_default,
            visible=toggle_show_visible)
        self.render_lines_checkbox = ipywidgets.Checkbox(
            description=render_checkbox_title,
            value=line_options_default['render_lines'])
        self.line_width_text = ipywidgets.BoundedFloatText(
            description='Width', value=line_options_default['line_width'],
            min=0., max=10 ** 6)
        line_style_dict = OrderedDict()
        line_style_dict['solid'] = '-'
        line_style_dict['dashed'] = '--'
        line_style_dict['dash-dot'] = '-.'
        line_style_dict['dotted'] = ':'
        self.line_style_dropdown = ipywidgets.Dropdown(
            options=line_style_dict, value=line_options_default['line_style'],
            description='Style')
        self.line_colour_widget = ColourSelectionWidget(
            line_options_default['line_colour'], description='Colour',
            labels=labels, render_function=render_function)
        self.line_options_box = ipywidgets.Box(
            children=[self.line_style_dropdown, self.line_width_text,
                      self.line_colour_widget])
        self.options_box = ipywidgets.VBox(children=[self.render_lines_checkbox,
                                                     self.line_options_box],
                                           visible=toggle_show_default,
                                           align='end')
        super(LineOptionsWidget, self).__init__(children=[self.toggle_visible,
                                                          self.options_box])

        # Assign output
        self.selected_values = line_options_default

        # Set functionality
        def line_options_visible(name, value):
            self.line_style_dropdown.disabled = not value
            self.line_width_text.disabled = not value
            self.line_colour_widget.disabled(not value)
        line_options_visible('', line_options_default['render_lines'])
        self.render_lines_checkbox.on_trait_change(line_options_visible,
                                                   'value')

        def save_render_lines(name, value):
            self.selected_values['render_lines'] = value
        self.render_lines_checkbox.on_trait_change(save_render_lines, 'value')

        def save_line_width(name, value):
            self.selected_values['line_width'] = float(value)
        self.line_width_text.on_trait_change(save_line_width, 'value')

        def save_line_style(name, value):
            self.selected_values['line_style'] = value
        self.line_style_dropdown.on_trait_change(save_line_style, 'value')

        self.selected_values['line_colour'] = \
            self.line_colour_widget.selected_values['colour']

        def toggle_function(name, value):
            self.options_box.visible = value
        self.toggle_visible.on_trait_change(toggle_function, 'value')

        # Set render function
        self._render_function = None
        self.add_render_function(render_function)

    def style(self, outer_box_style=None, outer_border_visible=False,
              outer_border_color='black', outer_border_style='solid',
              outer_border_width=1, outer_padding=0, outer_margin=0,
              inner_box_style=None, inner_border_visible=True,
              inner_border_color='black', inner_border_style='solid',
              inner_border_width=1, inner_padding=0, inner_margin=0,
              font_family='', font_size=None, font_style='',
              font_weight=''):
        r"""
        Function that defines the styling of the widget.

        Parameters
        ----------
        outer_box_style : `str` or ``None`` (see below), optional
            Outer box style options ::

                {``'success'``, ``'info'``, ``'warning'``, ``'danger'``, ``''``}
                or
                ``None``

        outer_border_visible : `bool`, optional
            Defines whether to draw the border line around the outer box.
        outer_border_color : `str`, optional
            The color of the border around the outer box.
        outer_border_style : `str`, optional
            The line style of the border around the outer box.
        outer_border_width : `float`, optional
            The line width of the border around the outer box.
        outer_padding : `float`, optional
            The padding around the outer box.
        outer_margin : `float`, optional
            The margin around the outer box.
        inner_box_style : `str` or ``None`` (see below), optional
            Inner box style options ::

                {``'success'``, ``'info'``, ``'warning'``, ``'danger'``, ``''``}
                or
                ``None``

        inner_border_visible : `bool`, optional
            Defines whether to draw the border line around the inner box.
        inner_border_color : `str`, optional
            The color of the border around the inner box.
        inner_border_style : `str`, optional
            The line style of the border around the inner box.
        inner_border_width : `float`, optional
            The line width of the border around the inner box.
        inner_padding : `float`, optional
            The padding around the inner box.
        inner_margin : `float`, optional
            The margin around the inner box.
        font_family : See Below, optional
            The font family to be used.
            Example options ::

                {``'serif'``, ``'sans-serif'``, ``'cursive'``, ``'fantasy'``,
                 ``'monospace'``, ``'helvetica'``}

        font_size : `int`, optional
            The font size.
        font_style : {``'normal'``, ``'italic'``, ``'oblique'``}, optional
            The font style.
        font_weight : See Below, optional
            The font weight.
            Example options ::

                {``'ultralight'``, ``'light'``, ``'normal'``, ``'regular'``,
                 ``'book'``, ``'medium'``, ``'roman'``, ``'semibold'``,
                 ``'demibold'``, ``'demi'``, ``'bold'``, ``'heavy'``,
                 ``'extra bold'``, ``'black'``}

        slider_width : `str`, optional
            The width of the slider.
        """
        _format_box(self, outer_box_style, outer_border_visible,
                    outer_border_color, outer_border_style, outer_border_width,
                    outer_padding, outer_margin)
        _format_box(self.options_box, inner_box_style, inner_border_visible,
                    inner_border_color, inner_border_style, inner_border_width,
                    inner_padding, inner_margin)
        _format_font(self, font_family, font_size, font_style, font_weight)
        _format_font(self.render_lines_checkbox, font_family, font_size,
                     font_style, font_weight)
        _format_font(self.line_style_dropdown, font_family, font_size,
                     font_style, font_weight)
        _format_font(self.line_width_text, font_family, font_size, font_style,
                     font_weight)
        _format_font(self.toggle_visible, font_family, font_size, font_style,
                     font_weight)
        self.line_colour_widget.style(box_style=None, border_visible=False,
                                      font_family=font_family,
                                      font_size=font_size,
                                      font_weight=font_weight,
                                      font_style=font_style, rgb_width='1.0cm')

    def add_render_function(self, render_function):
        r"""
        Method that adds a `render_function()` to the widget. The signature of
        the given function is also stored in `self._render_function`.

        Parameters
        ----------
        render_function : `function` or ``None``, optional
            The render function that behaves as a callback. If ``None``, then
            nothing is added.
        """
        self._render_function = render_function
        if self._render_function is not None:
            self.render_lines_checkbox.on_trait_change(self._render_function,
                                                       'value')
            self.line_style_dropdown.on_trait_change(self._render_function,
                                                     'value')
            self.line_width_text.on_trait_change(self._render_function, 'value')
        self.line_colour_widget.add_render_function(render_function)

    def remove_render_function(self):
        r"""
        Method that removes the current `self._render_function()` from the
        widget and sets ``self._render_function = None``.
        """
        self.render_lines_checkbox.on_trait_change(self._render_function,
                                                   'value', remove=True)
        self.line_style_dropdown.on_trait_change(self._render_function, 'value',
                                                 remove=True)
        self.line_width_text.on_trait_change(self._render_function, 'value',
                                             remove=True)
        self.line_colour_widget.remove_render_function()
        self._render_function = None

    def replace_render_function(self, render_function):
        r"""
        Method that replaces the current `self._render_function()` of the widget
        with the given `render_function()`.

        Parameters
        ----------
        render_function : `function` or ``None``, optional
            The render function that behaves as a callback. If ``None``, then
            nothing is happening.
        """
        # remove old function
        self.remove_render_function()

        # add new function
        self.add_render_function(render_function)

    def set_widget_state(self, line_options_dict, labels=None,
                         allow_callback=True):
        r"""
        Method that updates the state of the widget, if the provided
        `line_options_dict` is different than `self.selected_values()`.

        Parameter
        ---------
        line_options_dict : `dict`
            The new set of options. For example ::

                line_options_dict = {'render_lines': True, 'line_width': 2,
                                     'line_colour': ['r'], 'line_style': '-'}

        labels : `list` or ``None``, optional
            A `list` with the labels' names that get passed in to the
            `ColourSelectionWidget`. If ``None``, then a `list` of the form
            ``label {}`` is automatically defined.
        allow_callback : `bool`, optional
            If ``True``, it allows triggering of any callback functions.
        """
        # Assign new options dict to selected_values
        self.selected_values = line_options_dict

        # temporarily remove render callback
        render_function = self._render_function
        self.remove_render_function()

        # update render lines checkbox
        if 'render_lines' in line_options_dict.keys():
            self.render_lines_checkbox.value = line_options_dict['render_lines']

        # update line_style dropdown menu
        if 'line_style' in line_options_dict.keys():
            self.line_style_dropdown.value = line_options_dict['line_style']

        # update line_width text box
        if 'line_width' in line_options_dict.keys():
            self.line_width_text.value = float(line_options_dict['line_width'])

        # re-assign render callback
        self.add_render_function(render_function)

        # update line_colour
        if 'line_colour' in line_options_dict.keys():
            self.line_colour_widget.set_widget_state(
                line_options_dict['line_colour'], labels=labels,
                allow_callback=False)

        # trigger render function if allowed
        if allow_callback:
            self._render_function('', True)


class MarkerOptionsWidget(ipywidgets.Box):
    r"""
    Creates a widget for selecting line rendering options. Specifically, it
    consists of:

        1) ToggleButton [`self.toggle_visible`]: toggle buttons that controls
           the options' visibility
        2) Checkbox [`self.render_markers_checkbox`]: whether to render markers
        3) BoundedIntText [`self.marker_size_text`]: sets the marker size
        4) BoundedFloatText [`self.marker_edge_width_text`]: sets the marker
           edge width
        5) Dropdown [`self.marker_style_dropdown`]: sets the marker style
        6) ColourSelectionWidget [`self.marker_edge_colour_widget`]: sets the
           marker edge colour
        7) ColourSelectionWidget [`self.marker_face_colour_widget`]: sets the
           marker face colour
        8) Box [`self.marker_options_box`]: box that contains (3), (4), (5),
           (6) and (7)
        9) Box [`self.options_box`]: box that contains (2) and (8)

    The selected values are stored in `self.selected_values` `dict`. To set the
    styling of this widget please refer to the `style()` method. To update the
    state and function of the widget, please refer to the `set_widget_state()`
    and `set_render_function()` methods.

    Parameters
    ----------
    marker_options_default : `dict`
        The initial marker options. Example ::

            marker_options_default = {'render_markers': True,
                                      'marker_size': 20,
                                      'marker_face_colour': ['r'],
                                      'marker_edge_colour': ['k'],
                                      'marker_style': 'o',
                                      'marker_edge_width': 1}

    render_function : `function` or ``None``, optional
        The render function that is executed when a widgets' value changes.
        If ``None``, then nothing is assigned.
    toggle_show_default : `bool`, optional
        Defines whether the options will be visible upon construction.
    toggle_show_visible : `bool`, optional
        The visibility of the toggle button.
    toggle_title : `str`, optional
        The title of the toggle button.
    render_checkbox_title : `str`, optional
        The description of the show marker checkbox.
    labels : `list` or ``None``, optional
        A `list` with the labels' names that get passed in to the
        `ColourSelectionWidget`. If ``None``, then a `list` of the form
        ``label {}`` is automatically defined. Note that the labels are defined
        only for the colour option and not the rest of the options.
    """
    def __init__(self, marker_options_default, render_function=None,
                 toggle_show_visible=True, toggle_show_default=True,
                 toggle_title='Marker Object',
                 render_checkbox_title='Render markers', labels=None):
        self.toggle_visible = ipywidgets.ToggleButton(
            description=toggle_title, value=toggle_show_default,
            visible=toggle_show_visible)
        self.render_markers_checkbox = ipywidgets.Checkbox(
            description=render_checkbox_title,
            value=marker_options_default['render_markers'])
        self.marker_size_text = ipywidgets.BoundedIntText(
            description='Size', value=marker_options_default['marker_size'],
            min=0, max=10**6)
        self.marker_edge_width_text = ipywidgets.BoundedFloatText(
            description='Edge width', min=0., max=10**6,
            value=marker_options_default['marker_edge_width'])
        marker_style_dict = OrderedDict()
        marker_style_dict['point'] = '.'
        marker_style_dict['pixel'] = ','
        marker_style_dict['circle'] = 'o'
        marker_style_dict['triangle down'] = 'v'
        marker_style_dict['triangle up'] = '^'
        marker_style_dict['triangle left'] = '<'
        marker_style_dict['triangle right'] = '>'
        marker_style_dict['tri down'] = '1'
        marker_style_dict['tri up'] = '2'
        marker_style_dict['tri left'] = '3'
        marker_style_dict['tri right'] = '4'
        marker_style_dict['octagon'] = '8'
        marker_style_dict['square'] = 's'
        marker_style_dict['pentagon'] = 'p'
        marker_style_dict['star'] = '*'
        marker_style_dict['hexagon 1'] = 'h'
        marker_style_dict['hexagon 2'] = 'H'
        marker_style_dict['plus'] = '+'
        marker_style_dict['x'] = 'x'
        marker_style_dict['diamond'] = 'D'
        marker_style_dict['thin diamond'] = 'd'
        self.marker_style_dropdown = ipywidgets.Dropdown(
            options=marker_style_dict,
            value=marker_options_default['marker_style'], description='Style')
        self.marker_face_colour_widget = ColourSelectionWidget(
            marker_options_default['marker_face_colour'],
            description='Face Colour', labels=labels,
            render_function=render_function)
        self.marker_edge_colour_widget = ColourSelectionWidget(
            marker_options_default['marker_edge_colour'],
            description='Edge Colour', labels=labels,
            render_function=render_function)
        self.marker_options_box = ipywidgets.Box(
            children=[self.marker_style_dropdown, self.marker_size_text,
                      self.marker_edge_width_text,
                      self.marker_face_colour_widget,
                      self.marker_edge_colour_widget])
        self.options_box = ipywidgets.VBox(
            children=[self.render_markers_checkbox, self.marker_options_box],
            visible=toggle_show_default, align='end')
        super(MarkerOptionsWidget, self).__init__(children=[self.toggle_visible,
                                                            self.options_box])

        # Assign output
        self.selected_values = marker_options_default

        # Set functionality
        def marker_options_visible(name, value):
            self.marker_style_dropdown.disabled = not value
            self.marker_size_text.disabled = not value
            self.marker_edge_width_text.disabled = not value
            self.marker_face_colour_widget.disabled(not value)
            self.marker_edge_colour_widget.disabled(not value)
        marker_options_visible('', marker_options_default['render_markers'])
        self.render_markers_checkbox.on_trait_change(marker_options_visible,
                                                     'value')

        def save_render_markers(name, value):
            self.selected_values['render_markers'] = value
        self.render_markers_checkbox.on_trait_change(save_render_markers,
                                                     'value')

        def save_marker_size(name, value):
            self.selected_values['marker_size'] = int(value)
        self.marker_size_text.on_trait_change(save_marker_size, 'value')

        def save_marker_edge_width(name, value):
            self.selected_values['marker_edge_width'] = float(value)
        self.marker_edge_width_text.on_trait_change(save_marker_edge_width,
                                                    'value')

        def save_marker_style(name, value):
            self.selected_values['marker_style'] = value
        self.marker_style_dropdown.on_trait_change(save_marker_style, 'value')

        self.selected_values['marker_edge_colour'] = \
            self.marker_edge_colour_widget.selected_values['colour']
        self.selected_values['marker_face_colour'] = \
            self.marker_face_colour_widget.selected_values['colour']

        def toggle_function(name, value):
            self.options_box.visible = value
        self.toggle_visible.on_trait_change(toggle_function, 'value')

        # Set render function
        self._render_function = None
        self.add_render_function(render_function)

    def style(self, outer_box_style=None, outer_border_visible=False,
              outer_border_color='black', outer_border_style='solid',
              outer_border_width=1, outer_padding=0, outer_margin=0,
              inner_box_style=None, inner_border_visible=True,
              inner_border_color='black', inner_border_style='solid',
              inner_border_width=1, inner_padding=0, inner_margin=0,
              font_family='', font_size=None, font_style='',
              font_weight=''):
        r"""
        Function that defines the styling of the widget.

        Parameters
        ----------
        outer_box_style : `str` or ``None`` (see below), optional
            Outer box style options ::

                {``'success'``, ``'info'``, ``'warning'``, ``'danger'``, ``''``}
                or
                ``None``

        outer_border_visible : `bool`, optional
            Defines whether to draw the border line around the outer box.
        outer_border_color : `str`, optional
            The color of the border around the outer box.
        outer_border_style : `str`, optional
            The line style of the border around the outer box.
        outer_border_width : `float`, optional
            The line width of the border around the outer box.
        outer_padding : `float`, optional
            The padding around the outer box.
        outer_margin : `float`, optional
            The margin around the outer box.
        inner_box_style : `str` or ``None`` (see below), optional
            Inner box style options ::

                {``'success'``, ``'info'``, ``'warning'``, ``'danger'``, ``''``}
                or
                ``None``

        inner_border_visible : `bool`, optional
            Defines whether to draw the border line around the inner box.
        inner_border_color : `str`, optional
            The color of the border around the inner box.
        inner_border_style : `str`, optional
            The line style of the border around the inner box.
        inner_border_width : `float`, optional
            The line width of the border around the inner box.
        inner_padding : `float`, optional
            The padding around the inner box.
        inner_margin : `float`, optional
            The margin around the inner box.
        font_family : See Below, optional
            The font family to be used.
            Example options ::

                {``'serif'``, ``'sans-serif'``, ``'cursive'``, ``'fantasy'``,
                 ``'monospace'``, ``'helvetica'``}

        font_size : `int`, optional
            The font size.
        font_style : {``'normal'``, ``'italic'``, ``'oblique'``}, optional
            The font style.
        font_weight : See Below, optional
            The font weight.
            Example options ::

                {``'ultralight'``, ``'light'``, ``'normal'``, ``'regular'``,
                 ``'book'``, ``'medium'``, ``'roman'``, ``'semibold'``,
                 ``'demibold'``, ``'demi'``, ``'bold'``, ``'heavy'``,
                 ``'extra bold'``, ``'black'``}

        slider_width : `str`, optional
            The width of the slider.
        """
        _format_box(self, outer_box_style, outer_border_visible,
                    outer_border_color, outer_border_style, outer_border_width,
                    outer_padding, outer_margin)
        _format_box(self.options_box, inner_box_style, inner_border_visible,
                    inner_border_color, inner_border_style, inner_border_width,
                    inner_padding, inner_margin)
        _format_font(self, font_family, font_size, font_style, font_weight)
        _format_font(self.render_markers_checkbox, font_family, font_size,
                     font_style, font_weight)
        _format_font(self.marker_style_dropdown, font_family, font_size,
                     font_style, font_weight)
        _format_font(self.marker_size_text, font_family, font_size, font_style,
                     font_weight)
        _format_font(self.marker_edge_width_text, font_family, font_size,
                     font_style, font_weight)
        _format_font(self.toggle_visible, font_family, font_size, font_style,
                     font_weight)
        self.marker_edge_colour_widget.style(
            box_style=None, border_visible=False, font_family=font_family,
            font_size=font_size, font_weight=font_weight, font_style=font_style,
            rgb_width='1.0cm')
        self.marker_face_colour_widget.style(
            box_style=None, border_visible=False, font_family=font_family,
            font_size=font_size, font_weight=font_weight, font_style=font_style,
            rgb_width='1.0cm')

    def add_render_function(self, render_function):
        r"""
        Method that adds a `render_function()` to the widget. The signature of
        the given function is also stored in `self._render_function`.

        Parameters
        ----------
        render_function : `function` or ``None``, optional
            The render function that behaves as a callback. If ``None``, then
            nothing is added.
        """
        self._render_function = render_function
        if self._render_function is not None:
            self.render_markers_checkbox.on_trait_change(self._render_function,
                                                         'value')
            self.marker_style_dropdown.on_trait_change(self._render_function,
                                                       'value')
            self.marker_edge_width_text.on_trait_change(self._render_function,
                                                        'value')
            self.marker_size_text.on_trait_change(self._render_function,
                                                  'value')
        self.marker_edge_colour_widget.add_render_function(render_function)
        self.marker_face_colour_widget.add_render_function(render_function)

    def remove_render_function(self):
        r"""
        Method that removes the current `self._render_function()` from the
        widget and sets ``self._render_function = None``.
        """
        self.render_markers_checkbox.on_trait_change(self._render_function,
                                                     'value', remove=True)
        self.marker_style_dropdown.on_trait_change(self._render_function,
                                                   'value', remove=True)
        self.marker_edge_width_text.on_trait_change(self._render_function,
                                                    'value', remove=True)
        self.marker_size_text.on_trait_change(self._render_function, 'value',
                                              remove=True)
        self.marker_edge_colour_widget.remove_render_function()
        self.marker_face_colour_widget.remove_render_function()
        self._render_function = None

    def replace_render_function(self, render_function):
        r"""
        Method that replaces the current `self._render_function()` of the widget
        with the given `render_function()`.

        Parameters
        ----------
        render_function : `function` or ``None``, optional
            The render function that behaves as a callback. If ``None``, then
            nothing is happening.
        """
        # remove old function
        self.remove_render_function()

        # add new function
        self.add_render_function(render_function)

    def set_widget_state(self, marker_options_dict, labels=None,
                         allow_callback=True):
        r"""
        Method that updates the state of the widget, if the provided
        `marker_options_dict` is different than `self.selected_values()`.

        Parameter
        ---------
        marker_options_dict : `dict`
            The new set of options. For example ::

                marker_options_dict = {'render_markers': True,
                                       'marker_size': 20,
                                       'marker_face_colour': ['r'],
                                       'marker_edge_colour': ['k'],
                                       'marker_style': 'o',
                                       'marker_edge_width': 1}

        labels : `list` or ``None``, optional
            A `list` with the labels' names that get passed in to the
            `ColourSelectionWidget`. If ``None``, then a `list` of the form
            ``label {}`` is automatically defined.
        allow_callback : `bool`, optional
            If ``True``, it allows triggering of any callback functions.
        """
        # Assign new options dict to selected_values
        self.selected_values = marker_options_dict

        # temporarily remove render callback
        render_function = self._render_function
        self.remove_render_function()

        # update render markers checkbox
        if 'render_markers' in marker_options_dict.keys():
            self.render_markers_checkbox.value = \
                marker_options_dict['render_markers']

        # update marker_style dropdown menu
        if 'marker_style' in marker_options_dict.keys():
            self.marker_style_dropdown.value = \
                marker_options_dict['marker_style']

        # update marker_size text box
        if 'marker_size' in marker_options_dict.keys():
            self.marker_size_text.value = \
                int(marker_options_dict['marker_size'])

        # update marker_edge_width text box
        if 'marker_edge_width' in marker_options_dict.keys():
            self.marker_edge_width_text.value = \
                float(marker_options_dict['marker_edge_width'])

        # re-assign render callback
        self.add_render_function(render_function)

        # update marker_face_colour
        if 'marker_face_colour' in marker_options_dict.keys():
            self.marker_face_colour_widget.set_widget_state(
                marker_options_dict['marker_face_colour'], labels=labels,
                allow_callback=False)

        # update marker_edge_colour
        if 'marker_edge_colour' in marker_options_dict.keys():
            self.marker_edge_colour_widget.set_widget_state(
                marker_options_dict['marker_edge_colour'], labels=labels,
                allow_callback=False)

        # trigger render function if allowed
        if allow_callback:
            self._render_function('', True)


def numbering_options(numbers_options_default, plot_function=None,
                      toggle_show_visible=True, toggle_show_default=True,
                      toggle_title='Numbering Options',
                      show_checkbox_title='Render numbering'):
    r"""
    Creates a widget with Numbering Options. Specifically, it has:
        1) A checkbox that controls text's visibility.
        2) A dropdown menu for font name.
        3) A bounded int text box for font size.
        4) A dropdown menu for font style.
        5) A dropdown menu for font weight.
        6) A colour_selection widget for font colour.
        7) A dropdown menu for horizontal alignment.
        8) A dropdown menu for vertical alignment.
        9) A toggle button that controls the visibility of all the above, i.e.
           the numbering options.

    The structure of the widgets is the following:
        numbering_options_wid.children = [toggle_button, options]
        options.children = [show_font_checkbox, other_options]
        other_options.children = [font_name, font_size, font_style, font_weight,
                                  font_colour, horizontal_align, vertical_align]

    The returned widget saves the selected values in the following dictionary:
        numbering_options_wid.selected_values

    To fix the alignment within this widget please refer to
    `format_numbering_options()` function.

    Parameters
    ----------
    numbers_options_default : `dict`
        The initial selected font options.
        Example:
            numbers_options_default = {'render_numbering': True,
                                       'numbers_font_name': 'serif',
                                       'numbers_font_size': 10,
                                       'numbers_font_style': 'normal',
                                       'numbers_font_weight': 'normal',
                                       'numbers_font_colour': ['k'],
                                       'numbers_horizontal_align': 'center',
                                       'numbers_vertical_align': 'bottom'}
    plot_function : `function` or None, optional
        The plot function that is executed when a widgets' value changes.
        If None, then nothing is assigned.
    toggle_show_default : `boolean`, optional
        Defines whether the options will be visible upon construction.
    toggle_show_visible : `boolean`, optional
        The visibility of the toggle button.
    toggle_title : `str`, optional
        The title of the toggle button.
    show_checkbox_title : `str`, optional
        The description of the show text checkbox.
    """
    import IPython.html.widgets as ipywidgets
    # Create widgets
    # toggle button
    but = ipywidgets.ToggleButton(description=toggle_title,
                                        value=toggle_show_default,
                                        visible=toggle_show_visible)

    # numbers_font_name, numbers_font_size, numbers_font_style,
    # numbers_font_weight, numbers_font_colour
    render_numbering = ipywidgets.Checkbox(
        description=show_checkbox_title,
        value=numbers_options_default['render_numbering'])
    numbers_font_name_dict = OrderedDict()
    numbers_font_name_dict['serif'] = 'serif'
    numbers_font_name_dict['sans-serif'] = 'sans-serif'
    numbers_font_name_dict['cursive'] = 'cursive'
    numbers_font_name_dict['fantasy'] = 'fantasy'
    numbers_font_name_dict['monospace'] = 'monospace'
    numbers_font_name = ipywidgets.Dropdown(
        options=numbers_font_name_dict,
        value=numbers_options_default['numbers_font_name'],
        description='Font')
    numbers_font_size = ipywidgets.BoundedIntText(
        description='Size', value=numbers_options_default['numbers_font_size'],
        min=2)
    numbers_font_style_dict = OrderedDict()
    numbers_font_style_dict['normal'] = 'normal'
    numbers_font_style_dict['italic'] = 'italic'
    numbers_font_style_dict['oblique'] = 'oblique'
    numbers_font_style = ipywidgets.Dropdown(
        options=numbers_font_style_dict,
        value=numbers_options_default['numbers_font_style'],
        description='Style')
    numbers_font_weight_dict = OrderedDict()
    numbers_font_weight_dict['normal'] = 'normal'
    numbers_font_weight_dict['ultralight'] = 'ultralight'
    numbers_font_weight_dict['light'] = 'light'
    numbers_font_weight_dict['regular'] = 'regular'
    numbers_font_weight_dict['book'] = 'book'
    numbers_font_weight_dict['medium'] = 'medium'
    numbers_font_weight_dict['roman'] = 'roman'
    numbers_font_weight_dict['semibold'] = 'semibold'
    numbers_font_weight_dict['demibold'] = 'demibold'
    numbers_font_weight_dict['demi'] = 'demi'
    numbers_font_weight_dict['bold'] = 'bold'
    numbers_font_weight_dict['heavy'] = 'heavy'
    numbers_font_weight_dict['extra bold'] = 'extra bold'
    numbers_font_weight_dict['black'] = 'black'
    numbers_font_weight = ipywidgets.Dropdown(
        options=numbers_font_weight_dict,
        value=numbers_options_default['numbers_font_weight'],
        description='Weight')
    numbers_font_colour = colour_selection(
        numbers_options_default['numbers_font_colour'], title='Colour',
        plot_function=plot_function)
    numbers_horizontal_align_dict = OrderedDict()
    numbers_horizontal_align_dict['center'] = 'center'
    numbers_horizontal_align_dict['right'] = 'right'
    numbers_horizontal_align_dict['left'] = 'left'
    numbers_horizontal_align = ipywidgets.Dropdown(
        options=numbers_horizontal_align_dict,
        value=numbers_options_default['numbers_horizontal_align'],
        description='Align hor.')
    numbers_vertical_align_dict = OrderedDict()
    numbers_vertical_align_dict['center'] = 'center'
    numbers_vertical_align_dict['top'] = 'top'
    numbers_vertical_align_dict['bottom'] = 'bottom'
    numbers_vertical_align_dict['baseline'] = 'baseline'
    numbers_vertical_align = ipywidgets.Dropdown(
        options=numbers_vertical_align_dict,
        value=numbers_options_default['numbers_vertical_align'],
        description='Align ver.')

    # Options widget
    all_font_options = ipywidgets.Box(
        children=[numbers_font_name, numbers_font_size, numbers_font_style,
                  numbers_font_weight, numbers_font_colour,
                  numbers_horizontal_align, numbers_vertical_align])
    options_wid = ipywidgets.Box(
        children=[render_numbering, all_font_options])

    # Final widget
    numbering_options_wid = ipywidgets.Box(
        children=[but, options_wid])

    # Assign output
    numbering_options_wid.selected_values = numbers_options_default

    # font options visibility
    def options_visible(name, value):
        numbers_font_name.disabled = not value
        numbers_font_size.disabled = not value
        numbers_font_style.disabled = not value
        numbers_font_weight.disabled = not value
        numbers_font_colour.children[0].children[0].disabled = not value
        numbers_font_colour.children[0].children[1].disabled = not value
        numbers_font_colour.children[1].disabled = not value
        numbers_font_colour.children[2].children[0].disabled = not value
        numbers_font_colour.children[2].children[1].disabled = not value
        numbers_font_colour.children[2].children[2].disabled = not value
        numbers_horizontal_align.disabled = not value
        numbers_vertical_align.disabled = not value
    options_visible('', numbers_options_default['render_numbering'])
    render_numbering.on_trait_change(options_visible, 'value')

    # get options functions
    def save_render_numbering(name, value):
        numbering_options_wid.selected_values['render_numbering'] = value
    render_numbering.on_trait_change(save_render_numbering, 'value')

    def save_numbers_font_name(name, value):
        numbering_options_wid.selected_values['numbers_font_name'] = value
    numbers_font_name.on_trait_change(save_numbers_font_name, 'value')

    def save_numbers_font_size(name, value):
        numbering_options_wid.selected_values['numbers_font_size'] = int(value)
    numbers_font_size.on_trait_change(save_numbers_font_size, 'value')

    def save_numbers_font_style(name, value):
        numbering_options_wid.selected_values['numbers_font_style'] = value
    numbers_font_style.on_trait_change(save_numbers_font_style, 'value')

    def save_numbers_font_weight(name, value):
        numbering_options_wid.selected_values['numbers_font_weight'] = value
    numbers_font_weight.on_trait_change(save_numbers_font_weight, 'value')

    def save_numbers_horizontal_align(name, value):
        numbering_options_wid.selected_values['numbers_horizontal_align'] = \
            value
    numbers_horizontal_align.on_trait_change(save_numbers_horizontal_align,
                                             'value')

    def save_numbers_vertical_align(name, value):
        numbering_options_wid.selected_values['numbers_vertical_align'] = value
    numbers_vertical_align.on_trait_change(save_numbers_vertical_align, 'value')

    numbering_options_wid.selected_values['numbers_font_colour'] = \
        numbers_font_colour.selected_values['colour']

    # Toggle button function
    def toggle_fun(name, value):
        options_wid.visible = value
    toggle_fun('', toggle_show_default)
    but.on_trait_change(toggle_fun, 'value')

    # assign plot_function
    if plot_function is not None:
        render_numbering.on_trait_change(plot_function, 'value')
        numbers_font_name.on_trait_change(plot_function, 'value')
        numbers_font_style.on_trait_change(plot_function, 'value')
        numbers_font_size.on_trait_change(plot_function, 'value')
        numbers_font_weight.on_trait_change(plot_function, 'value')
        numbers_horizontal_align.on_trait_change(plot_function, 'value')
        numbers_vertical_align.on_trait_change(plot_function, 'value')

    return numbering_options_wid


def format_numbering_options(numbering_options_wid, container_padding='6px',
                             container_margin='6px',
                             container_border='1px solid black',
                             toggle_button_font_weight='bold',
                             border_visible=True,
                             suboptions_border_visible=True):
    r"""
    Function that corrects the align (style format) of a given numbering_options
    widget. Usage example:
        numbering_options_wid = numbering_options()
        display(numbering_options_wid)
        format_numbering_options(numbering_options_wid)

    Parameters
    ----------
    numbering_options_wid :
        The widget object generated by the `numbering_options()` function.
    container_padding : `str`, optional
        The padding around the widget, e.g. '6px'
    container_margin : `str`, optional
        The margin around the widget, e.g. '6px'
    container_border : `str`, optional
        The border around the widget, e.g. '1px solid black'
    toggle_button_font_weight : `str`
        The font weight of the toggle button, e.g. 'bold'
    border_visible : `boolean`, optional
        Defines whether to draw the border line around the widget.
    suboptions_border_visible : `boolean`, optional
        Defines whether to draw the border line around the font options, under
        the show font checkbox.
    """
    # align font options with checkbox
    add_class(numbering_options_wid.children[1], 'align-end')

    # set fontsize text box width
    numbering_options_wid.children[1].children[1].children[1].width = '1cm'

    # format colour options
    format_colour_selection(
        numbering_options_wid.children[1].children[1].children[4])

    # border around options
    if suboptions_border_visible:
        numbering_options_wid.children[1].children[1].border = container_border

    # set toggle button font bold
    numbering_options_wid.children[0].font_weight = toggle_button_font_weight

    # margin and border around container widget
    numbering_options_wid.padding = container_padding
    numbering_options_wid.margin = container_margin
    if border_visible:
        numbering_options_wid.border = container_border


def update_numbering_options(numbering_options_wid, numbering_options_dict):
    r"""
    Function that updates the state of a given numbering_options widget. Usage
    example:
        numbering_options_default = {'render_numbering': True,
                                      'numbers_font_name': 'serif',
                                      'numbers_font_size': 10,
                                      'numbers_font_style': 'normal',
                                      'numbers_font_weight': 'normal',
                                      'numbers_font_colour': ['k'],
                                      'numbers_horizontal_align': 'center',
                                      'numbers_vertical_align': 'bottom'}
        numbering_options_wid = numbering_options(numbering_options_default)
        display(numbering_options_wid)
        format_numbering_options(numbering_options_wid)
        numbering_options_default = {'render_numbering': False,
                                      'numbers_font_name': 'serif',
                                      'numbers_font_size': 10,
                                      'numbers_font_style': 'normal',
                                      'numbers_font_weight': 'normal',
                                      'numbers_font_colour': ['k'],
                                      'numbers_horizontal_align': 'center',
                                      'numbers_vertical_align': 'bottom'}
        update_numbering_options(numbering_options_wid,
                                 numbering_options_default)

    Parameters
    ----------
    numbering_options_wid :
        The widget object generated by the `numbering_options()` function.
    numbering_options_dict : `dict`
        The new set of options. For example:
            numbering_options_dict = {'render_numbering': True,
                                      'numbers_font_name': 'serif',
                                      'numbers_font_size': 10,
                                      'numbers_font_style': 'normal',
                                      'numbers_font_weight': 'normal',
                                      'numbers_font_colour': ['k'],
                                      'numbers_horizontal_align': 'center',
                                      'numbers_vertical_align': 'bottom'}
    """
    # Assign new options dict to selected_values
    numbering_options_wid.selected_values = numbering_options_dict

    # update render numbering checkbox
    if 'render_numbering' in numbering_options_dict.keys():
        numbering_options_wid.children[1].children[0].value = \
            numbering_options_dict['render_numbering']

    # update numbers_font_name dropdown menu
    if 'numbers_font_name' in numbering_options_dict.keys():
        numbering_options_wid.children[1].children[1].children[0].value = \
            numbering_options_dict['numbers_font_name']

    # update numbers_font_size text box
    if 'numbers_font_size' in numbering_options_dict.keys():
        numbering_options_wid.children[1].children[1].children[1].value = \
            int(numbering_options_dict['numbers_font_size'])

    # update numbers_font_style dropdown menu
    if 'numbers_font_style' in numbering_options_dict.keys():
        numbering_options_wid.children[1].children[1].children[2].value = \
            numbering_options_dict['numbers_font_style']

    # update numbers_font_weight dropdown menu
    if 'numbers_font_weight' in numbering_options_dict.keys():
        numbering_options_wid.children[1].children[1].children[3].value = \
            numbering_options_dict['numbers_font_weight']

    # update numbers_font_colour
    if 'numbers_font_colour' in numbering_options_dict.keys():
        update_colour_selection(
            numbering_options_wid.children[1].children[1].children[4],
            numbering_options_dict['numbers_font_colour'])

    # update numbers_horizontal_align dropdown menu
    if 'numbers_horizontal_align' in numbering_options_dict.keys():
        numbering_options_wid.children[1].children[1].children[5].value = \
            numbering_options_dict['numbers_horizontal_align']

    # update numbers_vertical_align dropdown menu
    if 'numbers_vertical_align' in numbering_options_dict.keys():
        numbering_options_wid.children[1].children[1].children[6].value = \
            numbering_options_dict['numbers_vertical_align']


def figure_options(figure_options_default, plot_function=None,
                   figure_scale_bounds=(0.1, 4), figure_scale_step=0.1,
                   figure_scale_visible=True, axes_visible=True,
                   toggle_show_default=True, toggle_show_visible=True):
    r"""
    Creates a widget with Figure Options. Specifically, it has:
        1) A slider that controls the scaling of the figure.
        2) A checkbox that controls the visibility of the figure's axes.
        3) Font options for the axes.
        4) A toggle button that controls the visibility of all the above, i.e.
           the figure options.

    The structure of the widgets is the following:
        figure_options_wid.children = [toggle_button, figure_scale_slider,
                                       show_axes_checkbox, axes_font_name,
                                       axes_font_size, axes_font_style,
                                       axes_font_weight, axes_x_limits,
                                       axes_y_limits]

    The returned widget saves the selected values in the following dictionary:
        figure_options_wid.selected_values

    To fix the alignment within this widget please refer to
    `format_figure_options()` function.

    Parameters
    ----------
    figure_options_default : `dict`
        The initial selected figure options.
        Example:
            figure_options_default = {'x_scale': 1.,
                                      'y_scale': 1.,
                                      'render_axes': True,
                                      'axes_font_name': 'serif',
                                      'axes_font_size': 10,
                                      'axes_font_style': 'normal',
                                      'axes_font_weight': 'normal',
                                      'axes_x_limits': None,
                                      'axes_y_limits': None}
    plot_function : `function` or None, optional
        The plot function that is executed when a widgets' value changes.
        If None, then nothing is assigned.
    figure_scale_bounds : (`float`, `float`), optional
        The range of scales that can be optionally applied to the figure.
    figure_scale_step : `float`, optional
        The step of the scale sliders.
    figure_scale_visible : `boolean`, optional
        The visibility of the figure scales sliders.
    show_axes_visible : `boolean`, optional
        The visibility of the axes checkbox.
    toggle_show_default : `boolean`, optional
        Defines whether the options will be visible upon construction.
    toggle_show_visible : `boolean`, optional
        The visibility of the toggle button.
    """
    import IPython.html.widgets as ipywidgets
    # Create widgets
    # toggle button
    but = ipywidgets.ToggleButton(description='Figure Options',
                                        value=toggle_show_default,
                                        visible=toggle_show_visible)

    # figure_scale, render_axes
    figure_scale = ipywidgets.FloatSlider(description='Figure scale:',
                                                value=figure_options_default[
                                                    'x_scale'],
                                                min=figure_scale_bounds[0],
                                                max=figure_scale_bounds[1],
                                                step=figure_scale_step,
                                                visible=figure_scale_visible)
    render_axes = ipywidgets.Checkbox(description='Render axes',
                                            value=figure_options_default[
                                                'render_axes'],
                                            visible=axes_visible)
    axes_font_name_dict = OrderedDict()
    axes_font_name_dict['serif'] = 'serif'
    axes_font_name_dict['sans-serif'] = 'sans-serif'
    axes_font_name_dict['cursive'] = 'cursive'
    axes_font_name_dict['fantasy'] = 'fantasy'
    axes_font_name_dict['monospace'] = 'monospace'
    axes_font_name = ipywidgets.Dropdown(
        options=axes_font_name_dict,
        value=figure_options_default['axes_font_name'],
        description='Font',
        visible=axes_visible)
    axes_font_size = ipywidgets.BoundedIntText(
        description='Size', value=figure_options_default['axes_font_size'],
        min=0, visible=axes_visible)
    axes_font_style_dict = OrderedDict()
    axes_font_style_dict['normal'] = 'normal'
    axes_font_style_dict['italic'] = 'italic'
    axes_font_style_dict['oblique'] = 'oblique'
    axes_font_style = ipywidgets.Dropdown(
        options=axes_font_style_dict,
        value=figure_options_default['axes_font_style'],
        description='Style', visible=axes_visible)
    axes_font_weight_dict = OrderedDict()
    axes_font_weight_dict['normal'] = 'normal'
    axes_font_weight_dict['ultralight'] = 'ultralight'
    axes_font_weight_dict['light'] = 'light'
    axes_font_weight_dict['regular'] = 'regular'
    axes_font_weight_dict['book'] = 'book'
    axes_font_weight_dict['medium'] = 'medium'
    axes_font_weight_dict['roman'] = 'roman'
    axes_font_weight_dict['semibold'] = 'semibold'
    axes_font_weight_dict['demibold'] = 'demibold'
    axes_font_weight_dict['demi'] = 'demi'
    axes_font_weight_dict['bold'] = 'bold'
    axes_font_weight_dict['heavy'] = 'heavy'
    axes_font_weight_dict['extra bold'] = 'extra bold'
    axes_font_weight_dict['black'] = 'black'
    axes_font_weight = ipywidgets.Dropdown(
        options=axes_font_weight_dict,
        value=figure_options_default['axes_font_weight'],
        description='Weight', visible=axes_visible)
    if figure_options_default['axes_x_limits'] is None:
        tmp1 = False
        tmp2 = 0.
        tmp3 = 100.
    else:
        tmp1 = True
        tmp2 = figure_options_default['axes_x_limits'][0]
        tmp3 = figure_options_default['axes_x_limits'][1]
    axes_x_limits_enable = ipywidgets.Checkbox(value=tmp1,
                                                     description='X limits')
    axes_x_limits_from = ipywidgets.FloatText(value=tmp2, description='')
    axes_x_limits_to = ipywidgets.FloatText(value=tmp3, description='')
    axes_x_limits = ipywidgets.Box(children=[axes_x_limits_enable,
                                                         axes_x_limits_from,
                                                         axes_x_limits_to])
    if figure_options_default['axes_y_limits'] is None:
        tmp1 = False
        tmp2 = 0.
        tmp3 = 100.
    else:
        tmp1 = True
        tmp2 = figure_options_default['axes_y_limits'][0]
        tmp3 = figure_options_default['axes_y_limits'][1]
    axes_y_limits_enable = ipywidgets.Checkbox(value=tmp1,
                                                     description='Y limits')
    axes_y_limits_from = ipywidgets.FloatText(value=tmp2, description='')
    axes_y_limits_to = ipywidgets.FloatText(value=tmp3, description='')
    axes_y_limits = ipywidgets.Box(children=[axes_y_limits_enable,
                                                         axes_y_limits_from,
                                                         axes_y_limits_to])

    # Final widget
    figure_options_wid = ipywidgets.Box(children=[but, figure_scale,
                                                              render_axes,
                                                              axes_font_name,
                                                              axes_font_size,
                                                              axes_font_style,
                                                              axes_font_weight,
                                                              axes_x_limits,
                                                              axes_y_limits])

    # Assign output
    figure_options_wid.selected_values = figure_options_default

    # font options visibility
    def options_visible(name, value):
        axes_font_name.disabled = not value
        axes_font_size.disabled = not value
        axes_font_style.disabled = not value
        axes_font_weight.disabled = not value
        axes_x_limits_enable.disabled = not value
        axes_y_limits_enable.disabled = not value
        if value:
            axes_x_limits_from.disabled = not axes_x_limits_enable.value
            axes_x_limits_to.disabled = not axes_x_limits_enable.value
            axes_y_limits_from.disabled = not axes_y_limits_enable.value
            axes_y_limits_to.disabled = not axes_y_limits_enable.value
        else:
            axes_x_limits_from.disabled = True
            axes_x_limits_to.disabled = True
            axes_y_limits_from.disabled = True
            axes_y_limits_to.disabled = True
    options_visible('', figure_options_default['render_axes'])
    render_axes.on_trait_change(options_visible, 'value')

    # get options functions
    def save_render_axes(name, value):
        figure_options_wid.selected_values['render_axes'] = value
    render_axes.on_trait_change(save_render_axes, 'value')

    def save_axes_font_name(name, value):
        figure_options_wid.selected_values['axes_font_name'] = value
    axes_font_name.on_trait_change(save_axes_font_name, 'value')

    def save_axes_font_size(name, value):
        figure_options_wid.selected_values['axes_font_size'] = int(value)
    axes_font_size.on_trait_change(save_axes_font_size, 'value')

    def save_axes_font_style(name, value):
        figure_options_wid.selected_values['axes_font_style'] = value
    axes_font_style.on_trait_change(save_axes_font_style, 'value')

    def save_axes_font_weight(name, value):
        figure_options_wid.selected_values['axes_font_weight'] = value
    axes_font_weight.on_trait_change(save_axes_font_weight, 'value')

    def axes_x_limits_disable(name, value):
        axes_x_limits_from.disabled = not value
        axes_x_limits_to.disabled = not value
    axes_x_limits_disable('', axes_x_limits_enable.value)
    axes_x_limits_enable.on_trait_change(axes_x_limits_disable, 'value')

    def axes_y_limits_disable(name, value):
        axes_y_limits_from.disabled = not value
        axes_y_limits_to.disabled = not value
    axes_y_limits_disable('', axes_y_limits_enable.value)
    axes_y_limits_enable.on_trait_change(axes_y_limits_disable, 'value')

    def save_axes_x_limits(name, value):
        if axes_x_limits_enable.value:
            figure_options_wid.selected_values['axes_x_limits'] = \
                (axes_x_limits_from.value, axes_x_limits_to.value)
        else:
            figure_options_wid.selected_values['axes_x_limits'] = None
    axes_x_limits_enable.on_trait_change(save_axes_x_limits, 'value')
    axes_x_limits_from.on_trait_change(save_axes_x_limits, 'value')
    axes_x_limits_to.on_trait_change(save_axes_x_limits, 'value')

    def save_axes_y_limits(name, value):
        if axes_y_limits_enable.value:
            figure_options_wid.selected_values['axes_y_limits'] = \
                (axes_y_limits_from.value, axes_y_limits_to.value)
        else:
            figure_options_wid.selected_values['axes_y_limits'] = None
    axes_y_limits_enable.on_trait_change(save_axes_y_limits, 'value')
    axes_y_limits_from.on_trait_change(save_axes_y_limits, 'value')
    axes_y_limits_to.on_trait_change(save_axes_y_limits, 'value')

    def save_scale(name, value):
        figure_options_wid.selected_values['x_scale'] = value
        figure_options_wid.selected_values['y_scale'] = value
    figure_scale.on_trait_change(save_scale, 'value')

    # Toggle button function
    def toggle_fun(name, value):
        figure_scale.visible = value
        render_axes.visible = value
        axes_font_name.visible = value
        axes_font_size.visible = value
        axes_font_style.visible = value
        axes_font_weight.visible = value
        axes_x_limits.visible = value
        axes_y_limits.visible = value
    toggle_fun('', toggle_show_default)
    but.on_trait_change(toggle_fun, 'value')

    # assign plot_function
    if plot_function is not None:
        figure_scale.on_trait_change(plot_function, 'value')
        render_axes.on_trait_change(plot_function, 'value')
        axes_font_name.on_trait_change(plot_function, 'value')
        axes_font_size.on_trait_change(plot_function, 'value')
        axes_font_style.on_trait_change(plot_function, 'value')
        axes_font_weight.on_trait_change(plot_function, 'value')
        axes_x_limits_from.on_trait_change(plot_function, 'value')
        axes_x_limits_to.on_trait_change(plot_function, 'value')
        axes_x_limits_enable.on_trait_change(plot_function, 'value')
        axes_y_limits_from.on_trait_change(plot_function, 'value')
        axes_y_limits_to.on_trait_change(plot_function, 'value')
        axes_y_limits_enable.on_trait_change(plot_function, 'value')

    return figure_options_wid


def format_figure_options(figure_options_wid, container_padding='6px',
                          container_margin='6px',
                          container_border='1px solid black',
                          toggle_button_font_weight='bold',
                          border_visible=True):
    r"""
    Function that corrects the align (style format) of a given figure_options
    widget. Usage example:
        figure_options_wid = figure_options()
        display(figure_options_wid)
        format_figure_options(figure_options_wid)

    Parameters
    ----------
    figure_options_wid :
        The widget object generated by the `figure_options()` function.
    container_padding : `str`, optional
        The padding around the widget, e.g. '6px'
    container_margin : `str`, optional
        The margin around the widget, e.g. '6px'
    container_border : `str`, optional
        The border around the widget, e.g. '1px solid black'
    toggle_button_font_weight : `str`
        The font weight of the toggle button, e.g. 'bold'
    border_visible : `boolean`, optional
        Defines whether to draw the border line around the widget.
    """
    # fix figure scale slider width
    figure_options_wid.children[1].width = '3cm'

    # fix font size width
    figure_options_wid.children[4].width = '1cm'

    # align and set width of axes_x_limits
    remove_class(figure_options_wid.children[7], 'vbox')
    add_class(figure_options_wid.children[7], 'hbox')
    figure_options_wid.children[7].children[1].width = '1cm'
    figure_options_wid.children[7].children[2].width = '1cm'

    # align and set width of axes_y_limits
    remove_class(figure_options_wid.children[8], 'vbox')
    add_class(figure_options_wid.children[8], 'hbox')
    figure_options_wid.children[8].children[1].width = '1cm'
    figure_options_wid.children[8].children[2].width = '1cm'

    # set toggle button font bold
    figure_options_wid.children[0].font_weight = toggle_button_font_weight

    # margin and border around container widget
    figure_options_wid.padding = container_padding
    figure_options_wid.margin = container_margin
    if border_visible:
        figure_options_wid.border = container_border


def update_figure_options(figure_options_wid, figure_options_dict):
    r"""
    Function that updates the state of a given figure_options widget. Usage
    example:
        figure_options_default = {'x_scale': 1.,
                                  'y_scale': 1.,
                                  'render_axes': True,
                                  'axes_font_name': 'serif',
                                  'axes_font_size': 10,
                                  'axes_font_style': 'normal',
                                  'axes_font_weight': 'normal',
                                  'axes_x_limits': None,
                                  'axes_y_limits': None}
        figure_options_wid = figure_options(figure_options_default)
        display(figure_options_wid)
        format_figure_options(figure_options_wid)
        figure_options_default = {'x_scale': 1.,
                                  'y_scale': 1.,
                                  'render_axes': True,
                                  'axes_font_name': 'serif',
                                  'axes_font_size': 10,
                                  'axes_font_style': 'normal',
                                  'axes_font_weight': 'normal',
                                  'axes_x_limits': None,
                                  'axes_y_limits': None}
        update_figure_options(figure_options_wid, figure_options_default)

    Parameters
    ----------
    figure_options_wid :
        The widget object generated by the `figure_options()` function.
    figure_options_dict : `dict`
        The new set of options. For example:
            figure_options_dict = {'x_scale': 1.,
                                   'y_scale': 1.,
                                   'render_axes': True,
                                   'axes_font_name': 'serif',
                                   'axes_font_size': 10,
                                   'axes_font_style': 'normal',
                                   'axes_font_weight': 'normal',
                                   'axes_x_limits': None,
                                   'axes_y_limits': None}
    """
    # Assign new options dict to selected_values
    figure_options_wid.selected_values = figure_options_dict

    # update scale slider
    if 'x_scale' in figure_options_dict.keys():
        figure_options_wid.children[1].value = figure_options_dict['x_scale']
    elif 'y_scale' in figure_options_dict.keys():
        figure_options_wid.children[1].value = figure_options_dict['y_scale']

    # update render axes checkbox
    if 'render_axes' in figure_options_dict.keys():
        figure_options_wid.children[2].value = \
            figure_options_dict['render_axes']

    # update axes_font_name dropdown menu
    if 'axes_font_name' in figure_options_dict.keys():
        figure_options_wid.children[3].value = \
            figure_options_dict['axes_font_name']

    # update axes_font_size text box
    if 'axes_font_size' in figure_options_dict.keys():
        figure_options_wid.children[4].value = \
            int(figure_options_dict['axes_font_size'])

    # update axes_font_style dropdown menu
    if 'axes_font_style' in figure_options_dict.keys():
        figure_options_wid.children[5].value = \
            figure_options_dict['axes_font_style']

    # update axes_font_weight dropdown menu
    if 'axes_font_weight' in figure_options_dict.keys():
        figure_options_wid.children[6].value = \
            figure_options_dict['axes_font_weight']

    # update axes_x_limits
    if 'axes_x_limits' in figure_options_dict.keys():
        if figure_options_dict['axes_x_limits'] is None:
            tmp1 = False
            tmp2 = 0.
            tmp3 = 100.
        else:
            tmp1 = True
            tmp2 = figure_options_dict['axes_x_limits'][0]
            tmp3 = figure_options_dict['axes_x_limits'][1]
        figure_options_wid.children[7].children[0].value = tmp1
        figure_options_wid.children[7].children[1].value = tmp2
        figure_options_wid.children[7].children[2].value = tmp3

    # update axes_y_limits
    if 'axes_y_limits' in figure_options_dict.keys():
        if figure_options_dict['axes_y_limits'] is None:
            tmp1 = False
            tmp2 = 0.
            tmp3 = 100.
        else:
            tmp1 = True
            tmp2 = figure_options_dict['axes_y_limits'][0]
            tmp3 = figure_options_dict['axes_y_limits'][1]
        figure_options_wid.children[8].children[0].value = tmp1
        figure_options_wid.children[8].children[1].value = tmp2
        figure_options_wid.children[8].children[2].value = tmp3


def figure_options_two_scales(figure_options_default, plot_function=None,
                              coupled_default=False,
                              figure_scales_bounds=(0.1, 4),
                              figure_scales_step=0.1,
                              figure_scales_visible=True,
                              axes_visible=True, toggle_show_default=True,
                              toggle_show_visible=True):
    r"""
    Creates a widget with Figure Options. Specifically, it has:
        1) A slider that controls the scaling of the figure.
        2) A checkbox that controls the visibility of the figure's axes.
        3) Font options for the axes.
        4) A toggle button that controls the visibility of all the above, i.e.
           the figure options.

    The structure of the widgets is the following:
        figure_options_wid.children = [toggle_button, figure_scale_slider,
                                       show_axes_checkbox, axes_font_name,
                                       axes_font_size, axes_font_style,
                                       axes_font_weight, axes_x_limits,
                                       axes_y_limits]

    The returned widget saves the selected values in the following dictionary:
        figure_options_wid.selected_values

    To fix the alignment within this widget please refer to
    `format_figure_options()` function.

    Parameters
    ----------
    figure_options_default : `dict`
        The initial selected figure options.
        Example:
            figure_options_default = {'x_scale': 1.,
                                      'y_scale': 1.,
                                      'render_axes': True,
                                      'axes_font_name': 'serif',
                                      'axes_font_size': 10,
                                      'axes_font_style': 'normal',
                                      'axes_font_weight': 'normal',
                                      'axes_x_limits': None,
                                      'axes_y_limits': None}
    plot_function : `function` or None, optional
        The plot function that is executed when a widgets' value changes.
        If None, then nothing is assigned.
    figure_scale_bounds : (`float`, `float`), optional
        The range of scales that can be optionally applied to the figure.
    figure_scale_step : `float`, optional
        The step of the scale sliders.
    figure_scale_visible : `boolean`, optional
        The visibility of the figure scales sliders.
    show_axes_visible : `boolean`, optional
        The visibility of the axes checkbox.
    toggle_show_default : `boolean`, optional
        Defines whether the options will be visible upon construction.
    toggle_show_visible : `boolean`, optional
        The visibility of the toggle button.
    """
    import IPython.html.widgets as ipywidgets
    # Create widgets
    # toggle button
    but = ipywidgets.ToggleButton(description='Figure Options',
                                        value=toggle_show_default,
                                        visible=toggle_show_visible)

    # figure_scale, render_axes
    x_scale = ipywidgets.FloatSlider(description='Figure size: X scale',
                                           value=figure_options_default[
                                               'x_scale'],
                                           min=figure_scales_bounds[0],
                                           max=figure_scales_bounds[1],
                                           step=figure_scales_step)
    y_scale = ipywidgets.FloatSlider(description='Y scale',
                                           value=figure_options_default[
                                               'y_scale'],
                                           min=figure_scales_bounds[0],
                                           max=figure_scales_bounds[1],
                                           step=figure_scales_step,
                                           disabled=coupled_default)
    coupled = ipywidgets.Checkbox(description='Coupled',
                                        value=coupled_default)
    figure_scale = ipywidgets.Box(
        children=[x_scale, y_scale, coupled],
        visible=figure_scales_visible)
    render_axes = ipywidgets.Checkbox(description='Render axes',
                                            value=figure_options_default[
                                                'render_axes'],
                                            visible=axes_visible)
    axes_font_name_dict = OrderedDict()
    axes_font_name_dict['serif'] = 'serif'
    axes_font_name_dict['sans-serif'] = 'sans-serif'
    axes_font_name_dict['cursive'] = 'cursive'
    axes_font_name_dict['fantasy'] = 'fantasy'
    axes_font_name_dict['monospace'] = 'monospace'
    axes_font_name = ipywidgets.Dropdown(
        options=axes_font_name_dict,
        value=figure_options_default['axes_font_name'],
        description='Font',
        visible=axes_visible)
    axes_font_size = ipywidgets.BoundedIntText(
        description='Size', value=figure_options_default['axes_font_size'],
        min=0, visible=axes_visible)
    axes_font_style_dict = OrderedDict()
    axes_font_style_dict['normal'] = 'normal'
    axes_font_style_dict['italic'] = 'italic'
    axes_font_style_dict['oblique'] = 'oblique'
    axes_font_style = ipywidgets.Dropdown(
        options=axes_font_style_dict,
        value=figure_options_default['axes_font_style'],
        description='Style', visible=axes_visible)
    axes_font_weight_dict = OrderedDict()
    axes_font_weight_dict['normal'] = 'normal'
    axes_font_weight_dict['ultralight'] = 'ultralight'
    axes_font_weight_dict['light'] = 'light'
    axes_font_weight_dict['regular'] = 'regular'
    axes_font_weight_dict['book'] = 'book'
    axes_font_weight_dict['medium'] = 'medium'
    axes_font_weight_dict['roman'] = 'roman'
    axes_font_weight_dict['semibold'] = 'semibold'
    axes_font_weight_dict['demibold'] = 'demibold'
    axes_font_weight_dict['demi'] = 'demi'
    axes_font_weight_dict['bold'] = 'bold'
    axes_font_weight_dict['heavy'] = 'heavy'
    axes_font_weight_dict['extra bold'] = 'extra bold'
    axes_font_weight_dict['black'] = 'black'
    axes_font_weight = ipywidgets.Dropdown(
        options=axes_font_weight_dict,
        value=figure_options_default['axes_font_weight'],
        description='Weight', visible=axes_visible)
    if figure_options_default['axes_x_limits'] is None:
        tmp1 = False
        tmp2 = 0.
        tmp3 = 0.
    else:
        tmp1 = True
        tmp2 = figure_options_default['axes_x_limits'][0]
        tmp3 = figure_options_default['axes_x_limits'][1]
    axes_x_limits_enable = ipywidgets.Checkbox(value=tmp1,
                                                     description='X limits')
    axes_x_limits_from = ipywidgets.FloatText(value=tmp2, description='')
    axes_x_limits_to = ipywidgets.FloatText(value=tmp3, description='')
    axes_x_limits = ipywidgets.Box(children=[axes_x_limits_enable,
                                                         axes_x_limits_from,
                                                         axes_x_limits_to])
    if figure_options_default['axes_y_limits'] is None:
        tmp1 = False
        tmp2 = 0.
        tmp3 = 0.
    else:
        tmp1 = True
        tmp2 = figure_options_default['axes_y_limits'][0]
        tmp3 = figure_options_default['axes_y_limits'][1]
    axes_y_limits_enable = ipywidgets.Checkbox(value=tmp1,
                                                     description='Y limits')
    axes_y_limits_from = ipywidgets.FloatText(value=tmp2, description='')
    axes_y_limits_to = ipywidgets.FloatText(value=tmp3, description='')
    axes_y_limits = ipywidgets.Box(children=[axes_y_limits_enable,
                                                         axes_y_limits_from,
                                                         axes_y_limits_to])

    # Final widget
    figure_options_wid = ipywidgets.Box(children=[but, figure_scale,
                                                              render_axes,
                                                              axes_font_name,
                                                              axes_font_size,
                                                              axes_font_style,
                                                              axes_font_weight,
                                                              axes_x_limits,
                                                              axes_y_limits])

    # Assign output
    figure_options_wid.selected_values = figure_options_default

    # font options visibility
    def options_visible(name, value):
        axes_font_name.disabled = not value
        axes_font_size.disabled = not value
        axes_font_style.disabled = not value
        axes_font_weight.disabled = not value
        axes_x_limits.disabled = not value
        axes_y_limits.disabled = not value
    options_visible('', figure_options_default['render_axes'])
    render_axes.on_trait_change(options_visible, 'value')

    # Coupled sliders function
    def coupled_sliders(name, value):
        y_scale.disabled = value
    coupled_sliders('', coupled_default)
    coupled.on_trait_change(coupled_sliders, 'value')

    # get options functions
    def save_render_axes(name, value):
        figure_options_wid.selected_values['render_axes'] = value
    render_axes.on_trait_change(save_render_axes, 'value')

    def save_axes_font_name(name, value):
        figure_options_wid.selected_values['axes_font_name'] = value
    axes_font_name.on_trait_change(save_axes_font_name, 'value')

    def save_axes_font_size(name, value):
        figure_options_wid.selected_values['axes_font_size'] = int(value)
    axes_font_size.on_trait_change(save_axes_font_size, 'value')

    def save_axes_font_style(name, value):
        figure_options_wid.selected_values['axes_font_style'] = value
    axes_font_style.on_trait_change(save_axes_font_style, 'value')

    def save_axes_font_weight(name, value):
        figure_options_wid.selected_values['axes_font_weight'] = value
    axes_font_weight.on_trait_change(save_axes_font_weight, 'value')

    def axes_x_limits_disable(name, value):
        axes_x_limits_from.disabled = not value
        axes_x_limits_to.disabled = not value
    axes_x_limits_enable.on_trait_change(axes_x_limits_disable, 'value')

    def axes_y_limits_disable(name, value):
        axes_y_limits_from.disabled = not value
        axes_y_limits_to.disabled = not value
    axes_y_limits_enable.on_trait_change(axes_y_limits_disable, 'value')

    def save_axes_x_limits(name, value):
        if axes_x_limits_enable.value:
            figure_options_wid.selected_values['axes_x_limits'] = \
                (axes_x_limits_from.value, axes_x_limits_to.value)
        else:
            figure_options_wid.selected_values['axes_x_limits'] = None
    axes_x_limits_enable.on_trait_change(save_axes_x_limits, 'value')
    axes_x_limits_from.on_trait_change(save_axes_x_limits, 'value')
    axes_x_limits_to.on_trait_change(save_axes_x_limits, 'value')

    def save_axes_y_limits(name, value):
        if axes_y_limits_enable.value:
            figure_options_wid.selected_values['axes_y_limits'] = \
                (axes_y_limits_from.value, axes_y_limits_to.value)
        else:
            figure_options_wid.selected_values['axes_y_limits'] = None
    axes_y_limits_enable.on_trait_change(save_axes_y_limits, 'value')
    axes_y_limits_from.on_trait_change(save_axes_y_limits, 'value')
    axes_y_limits_to.on_trait_change(save_axes_y_limits, 'value')

    def save_x_scale(name, old_value, value):
        figure_options_wid.selected_values['x_scale'] = value
        if coupled.value:
            y_scale.value += value - old_value
    x_scale.on_trait_change(save_x_scale, 'value')

    def save_y_scale(name, value):
        figure_options_wid.selected_values['y_scale'] = value
    y_scale.on_trait_change(save_y_scale, 'value')

    # Toggle button function
    def toggle_fun(name, value):
        figure_scale.visible = value
        render_axes.visible = value
        axes_font_name.visible = value
        axes_font_size.visible = value
        axes_font_style.visible = value
        axes_font_weight.visible = value
        axes_x_limits.visible = value
        axes_y_limits.visible = value
    toggle_fun('', toggle_show_default)
    but.on_trait_change(toggle_fun, 'value')

    # assign plot_function
    if plot_function is not None:
        x_scale.on_trait_change(plot_function, 'value')
        y_scale.on_trait_change(plot_function, 'value')
        coupled.on_trait_change(plot_function, 'value')
        render_axes.on_trait_change(plot_function, 'value')
        axes_font_name.on_trait_change(plot_function, 'value')
        axes_font_size.on_trait_change(plot_function, 'value')
        axes_font_style.on_trait_change(plot_function, 'value')
        axes_font_weight.on_trait_change(plot_function, 'value')
        axes_x_limits_from.on_trait_change(plot_function, 'value')
        axes_x_limits_to.on_trait_change(plot_function, 'value')
        axes_x_limits_enable.on_trait_change(plot_function, 'value')
        axes_y_limits_from.on_trait_change(plot_function, 'value')
        axes_y_limits_to.on_trait_change(plot_function, 'value')
        axes_y_limits_enable.on_trait_change(plot_function, 'value')

    return figure_options_wid


def format_figure_options_two_scales(figure_options_wid,
                                     container_padding='6px',
                                     container_margin='6px',
                                     container_border='1px solid black',
                                     toggle_button_font_weight='bold',
                                     border_visible=True):
    r"""
    Function that corrects the align (style format) of a given
    figure_options_two_scales widget. Usage example:
        figure_options_wid = figure_options_two_scales()
        display(figure_options_wid)
        format_figure_options_two_scales(figure_options_wid)

    Parameters
    ----------
    figure_options_wid :
        The widget object generated by the `figure_options_two_scales()`
        function.
    container_padding : `str`, optional
        The padding around the widget, e.g. '6px'
    container_margin : `str`, optional
        The margin around the widget, e.g. '6px'
    container_border : `str`, optional
        The border around the widget, e.g. '1px solid black'
    toggle_button_font_weight : `str`
        The font weight of the toggle button, e.g. 'bold'
    border_visible : `boolean`, optional
        Defines whether to draw the border line around the widget.
    """
    # align figure scale sliders and checkbox
    # figure_options_wid.children[1].remove_class('vbox')
    # add_class(figure_options_wid.children[1], 'hbox')
    add_class(figure_options_wid.children[1], 'align-end')

    # fix figure scale sliders width
    figure_options_wid.children[1].children[0].width = '3cm'
    figure_options_wid.children[1].children[1].width = '3cm'

    # fix font size width
    figure_options_wid.children[4].width = '1cm'

    # align and set width of axes_x_limits
    remove_class(figure_options_wid.children[7], 'vbox')
    add_class(figure_options_wid.children[7], 'hbox')
    figure_options_wid.children[7].children[1].width = '1cm'
    figure_options_wid.children[7].children[2].width = '1cm'

    # align and set width of axes_y_limits
    remove_class(figure_options_wid.children[8], 'vbox')
    add_class(figure_options_wid.children[8], 'hbox')
    figure_options_wid.children[8].children[1].width = '1cm'
    figure_options_wid.children[8].children[2].width = '1cm'

    # set toggle button font bold
    figure_options_wid.children[0].font_weight = toggle_button_font_weight

    # margin and border around container widget
    figure_options_wid.padding = container_padding
    figure_options_wid.margin = container_margin
    if border_visible:
        figure_options_wid.border = container_border


def update_figure_options_two_scales(figure_options_wid, figure_options_dict):
    r"""
    Function that updates the state of a given figure_options_two_scales widget.
    Usage example:
        figure_options_default = {'x_scale': 1.,
                                  'y_scale': 1.,
                                  'render_axes': True,
                                  'axes_font_name': 'serif',
                                  'axes_font_size': 10,
                                  'axes_font_style': 'normal',
                                  'axes_font_weight': 'normal',
                                  'axes_x_limits': None,
                                  'axes_y_limits': None}
        figure_options_wid = figure_options_two_scales(default_figure_options)
        display(figure_options_wid)
        format_figure_options_two_scales(figure_options_wid)
        figure_options_default = {'x_scale': 1.,
                                  'y_scale': 1.,
                                  'render_axes': True,
                                  'axes_font_name': 'serif',
                                  'axes_font_size': 10,
                                  'axes_font_style': 'normal',
                                  'axes_font_weight': 'normal',
                                  'axes_x_limits': None,
                                  'axes_y_limits': None}
        update_figure_options_two_scales(figure_options_wid,
                                         default_figure_options)

    Parameters
    ----------
    figure_options_wid :
        The widget object generated by the `figure_options_two_scales()`
        function.
    figure_options_dict : `dict`
        The new set of options. For example:
            figure_options_default = {'x_scale': 1.,
                                      'y_scale': 1.,
                                      'render_axes': True,
                                      'axes_font_name': 'serif',
                                      'axes_font_size': 10,
                                      'axes_font_style': 'normal',
                                      'axes_font_weight': 'normal',
                                      'axes_x_limits': None,
                                      'axes_y_limits': None}
    """
    # Assign new options dict to selected_values
    figure_options_wid.selected_values = figure_options_dict

    # update scale slider
    if ('x_scale' in figure_options_dict.keys() and
            'y_scale' not in figure_options_dict.keys()):
        figure_options_wid.children[1].children[0].value = \
            figure_options_dict['x_scale']
        figure_options_wid.children[1].children[2].value = False
    elif ('x_scale' not in figure_options_dict.keys() and
            'y_scale' in figure_options_dict.keys()):
        figure_options_wid.children[1].children[1].value = \
            figure_options_dict['y_scale']
        figure_options_wid.children[1].children[2].value = False
    elif ('x_scale' in figure_options_dict.keys() and
            'y_scale' in figure_options_dict.keys()):
        figure_options_wid.children[1].children[0].value = \
            figure_options_dict['x_scale']
        figure_options_wid.children[1].children[1].value = \
            figure_options_dict['y_scale']
        figure_options_wid.children[1].children[2].value = \
            figure_options_dict['x_scale'] == figure_options_dict['y_scale']

    # update render axes checkbox
    if 'render_axes' in figure_options_dict.keys():
        figure_options_wid.children[2].value = \
            figure_options_dict['render_axes']

    # update axes_font_name dropdown menu
    if 'axes_font_name' in figure_options_dict.keys():
        figure_options_wid.children[3].value = \
            figure_options_dict['axes_font_name']

    # update axes_font_size text box
    if 'axes_font_size' in figure_options_dict.keys():
        figure_options_wid.children[4].value = \
            int(figure_options_dict['axes_font_size'])

    # update axes_font_style dropdown menu
    if 'axes_font_style' in figure_options_dict.keys():
        figure_options_wid.children[5].value = \
            figure_options_dict['axes_font_style']

    # update axes_font_weight dropdown menu
    if 'axes_font_weight' in figure_options_dict.keys():
        figure_options_wid.children[6].value = \
            figure_options_dict['axes_font_weight']

    # update axes_x_limits
    if 'axes_x_limits' in figure_options_dict.keys():
        if figure_options_dict['axes_x_limits'] is None:
            tmp1 = False
            tmp2 = 0.
            tmp3 = 0.
        else:
            tmp1 = True
            tmp2 = figure_options_dict['axes_x_limits'][0]
            tmp3 = figure_options_dict['axes_x_limits'][1]
        figure_options_wid.children[7].children[0].value = tmp1
        figure_options_wid.children[7].children[1].value = tmp2
        figure_options_wid.children[7].children[2].value = tmp3

    # update axes_y_limits
    if 'axes_y_limits' in figure_options_dict.keys():
        if figure_options_dict['axes_y_limits'] is None:
            tmp1 = False
            tmp2 = 0.
            tmp3 = 0.
        else:
            tmp1 = True
            tmp2 = figure_options_dict['axes_y_limits'][0]
            tmp3 = figure_options_dict['axes_y_limits'][1]
        figure_options_wid.children[8].children[0].value = tmp1
        figure_options_wid.children[8].children[1].value = tmp2
        figure_options_wid.children[8].children[2].value = tmp3


def legend_options(legend_options_default, plot_function=None,
                   toggle_show_visible=True, toggle_show_default=True,
                   toggle_title='Legend Options',
                   show_checkbox_title='Render legend'):
    r"""
    Creates a widget with Legend Options. Specifically, it has:
        1) A checkbox that controls legend's visibility.
        2) A tab widget with legend_location, font and formatting options.
        3) A toggle button that controls the visibility of all the above, i.e.
           the font options.

    The structure of the widgets is the following:
        legend_options_wid.children = [toggle_button, options]
        options.children = [show_legend_checkbox, other_options]
        other_options.children = [legend_location, font, formatting]
        ...

    The returned widget saves the selected values in the following dictionary:
        legend_options_wid.selected_values

    To fix the alignment within this widget please refer to
    `format_legend_options()` function.

    Parameters
    ----------
    legend_options_default : `dict`
        The initial selected font options.
        Example:
            legend_options_default = {'render_legend':True,
                                      'legend_title':'',
                                      'legend_font_name':'serif',
                                      'legend_font_style':'normal',
                                      'legend_font_size':10,
                                      'legend_font_weight':'normal',
                                      'legend_marker_scale':1.,
                                      'legend_location':2,
                                      'legend_bbox_to_anchor':(1.05, 1.),
                                      'legend_border_axes_pad':1.,
                                      'legend_n_columns':1,
                                      'legend_horizontal_spacing':1.,
                                      'legend_vertical_spacing':1.,
                                      'legend_border':True,
                                      'legend_border_padding':0.5,
                                      'legend_shadow':False,
                                      'legend_rounded_corners':True}
    plot_function : `function` or None, optional
        The plot function that is executed when a widgets' value changes.
        If None, then nothing is assigned.
    toggle_show_default : `boolean`, optional
        Defines whether the options will be visible upon construction.
    toggle_show_visible : `boolean`, optional
        The visibility of the toggle button.
    toggle_title : `str`, optional
        The legend_title of the toggle button.
    show_checkbox_title : `str`, optional
        The description of the show text checkbox.
    """
    import IPython.html.widgets as ipywidgets
    # Create widgets
    # toggle button
    but = ipywidgets.ToggleButton(description=toggle_title,
                                        value=toggle_show_default,
                                        visible=toggle_show_visible)

    # render legend
    render_legend = ipywidgets.Checkbox(
        description=show_checkbox_title,
        value=legend_options_default['render_legend'])

    # font-related
    legend_font_name_dict = OrderedDict()
    legend_font_name_dict['serif'] = 'serif'
    legend_font_name_dict['sans-serif'] = 'sans-serif'
    legend_font_name_dict['cursive'] = 'cursive'
    legend_font_name_dict['fantasy'] = 'fantasy'
    legend_font_name_dict['monospace'] = 'monospace'
    legend_font_name = ipywidgets.Dropdown(
        options=legend_font_name_dict,
        value=legend_options_default['legend_font_name'],
        description='Font')
    legend_font_size = ipywidgets.BoundedIntText(
        description='Size', value=legend_options_default['legend_font_size'],
        min=0)
    legend_font_style_dict = OrderedDict()
    legend_font_style_dict['normal'] = 'normal'
    legend_font_style_dict['italic'] = 'italic'
    legend_font_style_dict['oblique'] = 'oblique'
    legend_font_style = ipywidgets.Dropdown(
        options=legend_font_style_dict,
        value=legend_options_default['legend_font_style'],
        description='Style')
    legend_font_weight_dict = OrderedDict()
    legend_font_weight_dict['normal'] = 'normal'
    legend_font_weight_dict['ultralight'] = 'ultralight'
    legend_font_weight_dict['light'] = 'light'
    legend_font_weight_dict['regular'] = 'regular'
    legend_font_weight_dict['book'] = 'book'
    legend_font_weight_dict['medium'] = 'medium'
    legend_font_weight_dict['roman'] = 'roman'
    legend_font_weight_dict['semibold'] = 'semibold'
    legend_font_weight_dict['demibold'] = 'demibold'
    legend_font_weight_dict['demi'] = 'demi'
    legend_font_weight_dict['bold'] = 'bold'
    legend_font_weight_dict['heavy'] = 'heavy'
    legend_font_weight_dict['extra bold'] = 'extra bold'
    legend_font_weight_dict['black'] = 'black'
    legend_font_weight = ipywidgets.Dropdown(
        options=legend_font_weight_dict,
        value=legend_options_default['legend_font_weight'],
        description='Weight')
    legend_title = ipywidgets.Text(description='Title',
                                         value=legend_options_default[
                                             'legend_title'])
    font_cont_tmp = ipywidgets.Box(
        children=[ipywidgets.Box(children=[legend_font_name,
                                                       legend_font_size]),
                  ipywidgets.Box(children=[legend_font_style,
                                                       legend_font_weight])])
    font_cont = ipywidgets.Box(
        children=[legend_title, font_cont_tmp])

    # legend_location-related
    legend_location_dict = OrderedDict()
    legend_location_dict['best'] = 0
    legend_location_dict['upper right'] = 1
    legend_location_dict['upper left'] = 2
    legend_location_dict['lower left'] = 3
    legend_location_dict['lower right'] = 4
    legend_location_dict['right'] = 5
    legend_location_dict['center left'] = 6
    legend_location_dict['center right'] = 7
    legend_location_dict['lower center'] = 8
    legend_location_dict['upper center'] = 9
    legend_location_dict['center'] = 10
    legend_location = ipywidgets.Dropdown(
        options=legend_location_dict,
        value=legend_options_default['legend_location'],
        description='Predefined location')
    if legend_options_default['legend_bbox_to_anchor'] is None:
        tmp1 = False
        tmp2 = 0.
        tmp3 = 0.
    else:
        tmp1 = True
        tmp2 = legend_options_default['legend_bbox_to_anchor'][0]
        tmp3 = legend_options_default['legend_bbox_to_anchor'][1]
    bbox_to_anchor_enable = ipywidgets.Checkbox(
        value=tmp1, description='Arbitrary location')
    bbox_to_anchor_x = ipywidgets.FloatText(value=tmp2, description='')
    bbox_to_anchor_y = ipywidgets.FloatText(value=tmp3, description='')
    legend_bbox_to_anchor = ipywidgets.Box(
        children=[bbox_to_anchor_enable,
                  bbox_to_anchor_x,
                  bbox_to_anchor_y])
    legend_border_axes_pad = ipywidgets.BoundedFloatText(
        value=legend_options_default['legend_border_axes_pad'],
        description='Distance to axes', min=0.)
    location_cont = ipywidgets.Box(
        children=[legend_location, legend_bbox_to_anchor,
                  legend_border_axes_pad])

    # formatting-related
    legend_n_columns = ipywidgets.BoundedIntText(
        value=legend_options_default['legend_n_columns'], description='Columns',
        min=0)
    legend_marker_scale = ipywidgets.BoundedFloatText(
        description='Marker scale',
        value=legend_options_default['legend_marker_scale'], min=0.)
    legend_horizontal_spacing = ipywidgets.BoundedFloatText(
        value=legend_options_default['legend_horizontal_spacing'],
        description='Horizontal space', min=0.)
    legend_vertical_spacing = ipywidgets.BoundedFloatText(
        value=legend_options_default['legend_vertical_spacing'],
        description='Vertical space', min=0.)
    spacing = ipywidgets.Box(
        children=[ipywidgets.Box(children=[legend_n_columns,
                                                       legend_marker_scale]),
                  ipywidgets.Box(
                      children=[legend_horizontal_spacing,
                                legend_vertical_spacing])])
    legend_border = ipywidgets.Checkbox(
        description='Border',
        value=legend_options_default['legend_border'])
    legend_border_padding = ipywidgets.BoundedFloatText(
        value=legend_options_default['legend_border_padding'],
        description='Border pad', min=0.)
    border = ipywidgets.Box(
        children=[legend_border, legend_border_padding])
    legend_shadow = ipywidgets.Checkbox(
        description='Shadow', value=legend_options_default['legend_shadow'])
    legend_rounded_corners = ipywidgets.Checkbox(
        description='Rounded corners',
        value=legend_options_default['legend_rounded_corners'])
    shadow_fancy = ipywidgets.Box(children=[legend_shadow,
                                                        legend_rounded_corners])

    formatting_cont = ipywidgets.Box(
        children=[spacing, border, shadow_fancy])

    # Options widget
    tab_options = ipywidgets.Tab(children=[location_cont, font_cont,
                                                 formatting_cont])
    options_wid = ipywidgets.Box(
        children=[render_legend, tab_options])

    # Final widget
    legend_options_wid = ipywidgets.Box(children=[but, options_wid])

    # Assign output
    legend_options_wid.selected_values = legend_options_default

    # font options visibility
    def options_visible(name, value):
        legend_title.disabled = not value
        legend_font_name.disabled = not value
        legend_font_size.disabled = not value
        legend_font_style.disabled = not value
        legend_font_weight.disabled = not value
        legend_location.disabled = not value
        bbox_to_anchor_enable.disabled = not value
        bbox_to_anchor_x.disabled = not value or not bbox_to_anchor_enable.value
        bbox_to_anchor_y.disabled = not value or not bbox_to_anchor_enable.value
        legend_border_axes_pad.disabled = not value
        legend_n_columns.disabled = not value
        legend_marker_scale.disabled = not value
        legend_horizontal_spacing.disabled = not value
        legend_vertical_spacing.disabled = not value
        legend_border.disabled = not value
        legend_border_padding.disabled = not value or not legend_border.value
        legend_shadow.disabled = not value
        legend_rounded_corners.disabled = not value
    options_visible('', legend_options_default['render_legend'])
    render_legend.on_trait_change(options_visible, 'value')

    # get options functions
    def border_pad_disable(name, value):
        legend_border_padding.disabled = not value
    legend_border.on_trait_change(border_pad_disable, 'value')

    def bbox_to_anchor_disable(name, value):
        bbox_to_anchor_x.disabled = not value
        bbox_to_anchor_y.disabled = not value
    bbox_to_anchor_enable.on_trait_change(bbox_to_anchor_disable, 'value')

    def save_show_legend(name, value):
        legend_options_wid.selected_values['render_legend'] = value
    render_legend.on_trait_change(save_show_legend, 'value')

    def save_title(name, value):
        legend_options_wid.selected_values['legend_title'] = str(value)
    legend_title.on_trait_change(save_title, 'value')

    def save_fontname(name, value):
        legend_options_wid.selected_values['legend_font_name'] = value
    legend_font_name.on_trait_change(save_fontname, 'value')

    def save_fontsize(name, value):
        legend_options_wid.selected_values['legend_font_size'] = int(value)
    legend_font_size.on_trait_change(save_fontsize, 'value')

    def save_fontstyle(name, value):
        legend_options_wid.selected_values['legend_font_style'] = value
    legend_font_style.on_trait_change(save_fontstyle, 'value')

    def save_fontweight(name, value):
        legend_options_wid.selected_values['legend_font_weight'] = value
    legend_font_weight.on_trait_change(save_fontweight, 'value')

    def save_location(name, value):
        legend_options_wid.selected_values['legend_location'] = value
    legend_location.on_trait_change(save_location, 'value')

    def save_bbox_to_anchor(name, value):
        if bbox_to_anchor_enable.value:
            legend_options_wid.selected_values['legend_bbox_to_anchor'] = \
                (bbox_to_anchor_x.value, bbox_to_anchor_y.value)
        else:
            legend_options_wid.selected_values['legend_bbox_to_anchor'] = None
    bbox_to_anchor_enable.on_trait_change(save_bbox_to_anchor, 'value')
    bbox_to_anchor_x.on_trait_change(save_bbox_to_anchor, 'value')
    bbox_to_anchor_y.on_trait_change(save_bbox_to_anchor, 'value')

    def save_borderaxespad(name, value):
        key = 'legend_border_axes_pad'
        legend_options_wid.selected_values[key] = float(value)
    legend_border_axes_pad.on_trait_change(save_borderaxespad, 'value')

    def save_n_columns(name, value):
        legend_options_wid.selected_values['legend_n_columns'] = int(value)
    legend_n_columns.on_trait_change(save_n_columns, 'value')

    def save_markerscale(name, value):
        legend_options_wid.selected_values['legend_marker_scale'] = float(value)
    legend_marker_scale.on_trait_change(save_markerscale, 'value')

    def save_horizontal_spacing(name, value):
        legend_options_wid.selected_values['legend_horizontal_spacing'] = \
            float(value)
    legend_horizontal_spacing.on_trait_change(save_horizontal_spacing, 'value')

    def save_vertical_spacing(name, value):
        legend_options_wid.selected_values['legend_vertical_spacing'] = \
            float(value)
    legend_vertical_spacing.on_trait_change(save_vertical_spacing, 'value')

    def save_draw_border(name, value):
        legend_options_wid.selected_values['legend_border'] = value
    legend_border.on_trait_change(save_draw_border, 'value')

    def save_border_padding(name, value):
        legend_options_wid.selected_values['legend_border_padding'] = \
            float(value)
    legend_border_padding.on_trait_change(save_border_padding, 'value')

    def save_draw_shadow(name, value):
        legend_options_wid.selected_values['legend_shadow'] = value
    legend_shadow.on_trait_change(save_draw_shadow, 'value')

    def save_fancy_corners(name, value):
        legend_options_wid.selected_values['legend_rounded_corners'] = value
    legend_rounded_corners.on_trait_change(save_fancy_corners, 'value')

    # Toggle button function
    def toggle_fun(name, value):
        options_wid.visible = value
    toggle_fun('', toggle_show_default)
    but.on_trait_change(toggle_fun, 'value')

    # assign plot_function
    if plot_function is not None:
        render_legend.on_trait_change(plot_function, 'value')
        legend_title.on_trait_change(plot_function, 'value')
        legend_font_name.on_trait_change(plot_function, 'value')
        legend_font_style.on_trait_change(plot_function, 'value')
        legend_font_size.on_trait_change(plot_function, 'value')
        legend_font_weight.on_trait_change(plot_function, 'value')
        legend_location.on_trait_change(plot_function, 'value')
        bbox_to_anchor_enable.on_trait_change(plot_function, 'value')
        bbox_to_anchor_x.on_trait_change(plot_function, 'value')
        bbox_to_anchor_y.on_trait_change(plot_function, 'value')
        legend_border_axes_pad.on_trait_change(plot_function, 'value')
        legend_n_columns.on_trait_change(plot_function, 'value')
        legend_marker_scale.on_trait_change(plot_function, 'value')
        legend_horizontal_spacing.on_trait_change(plot_function, 'value')
        legend_vertical_spacing.on_trait_change(plot_function, 'value')
        legend_border.on_trait_change(plot_function, 'value')
        legend_border_padding.on_trait_change(plot_function, 'value')
        legend_shadow.on_trait_change(plot_function, 'value')
        legend_rounded_corners.on_trait_change(plot_function, 'value')

    return legend_options_wid


def format_legend_options(legend_options_wid, container_padding='6px',
                          container_margin='6px',
                          container_border='1px solid black',
                          toggle_button_font_weight='bold',
                          border_visible=True, suboptions_border_visible=False):
    r"""
    Function that corrects the align (style format) of a given legend_options
    widget. Usage example:
        legend_options_wid = legend_options()
        display(legend_options_wid)
        format_legend_options(legend_options_wid)

    Parameters
    ----------
    legend_options_wid :
        The widget object generated by the `legend_options()` function.
    container_padding : `str`, optional
        The padding around the widget, e.g. '6px'
    container_margin : `str`, optional
        The margin around the widget, e.g. '6px'
    container_border : `str`, optional
        The border around the widget, e.g. '1px solid black'
    toggle_button_font_weight : `str`
        The font weight of the toggle button, e.g. 'bold'
    border_visible : `boolean`, optional
        Defines whether to draw the border line around the widget.
    suboptions_border_visible : `boolean`, optional
        Defines whether to draw the border line around the legend options, under
        the show legend checkbox.
    """
    # set tab titles
    tab_titles = ['Location', 'Font', 'Formatting']
    for (k, tl) in enumerate(tab_titles):
        legend_options_wid.children[1].children[1].set_title(k, tl)

    # set fontsize and title text box width
    legend_options_wid.children[1].children[1].children[1].children[1].children[0].children[1].width = '1cm'
    legend_options_wid.children[1].children[1].children[1].children[0]. \
        width = '4cm'

    # align and set width of bbox_to_anchor
    remove_class(legend_options_wid.children[1].children[1].children[0].children[1], 'vbox')
    add_class(legend_options_wid.children[1].children[1].children[0].children[1], 'hbox')
    legend_options_wid.children[1].children[1].children[0].children[1].children[1]. \
        width = '1cm'
    legend_options_wid.children[1].children[1].children[0].children[1].children[2]. \
        width = '1cm'

    # set distance to axes (borderaxespad) text box width
    legend_options_wid.children[1].children[1].children[0].children[2]. \
        width = '1cm'

    # align and set width of border options
    remove_class(legend_options_wid.children[1].children[1].children[2].children[1], 'vbox')
    add_class(legend_options_wid.children[1].children[1].children[2].children[1], 'hbox')
    legend_options_wid.children[1].children[1].children[2].children[1].children[
        0]. \
        width = '1cm'
    legend_options_wid.children[1].children[1].children[2].children[1].children[
        1]. \
        width = '1cm'

    # align shadow and fancy checkboxes
    remove_class(legend_options_wid.children[1].children[1].children[2].children[2], 'vbox')
    add_class(legend_options_wid.children[1].children[1].children[2].children[2], 'hbox')

    # align and set width of spacing options
    add_class(legend_options_wid.children[1].children[1].children[2].children[0].children[1], 'align-end')
    legend_options_wid.children[1].children[1].children[2].children[0].children[
        1].children[0].width = '1cm'
    legend_options_wid.children[1].children[1].children[2].children[0].children[
        1].children[1].width = '1cm'

    # set width of n_columns and markerspace
    add_class(legend_options_wid.children[1].children[1].children[2].children[0].children[0], 'align-end')
    legend_options_wid.children[1].children[1].children[2].children[0].children[
        0].children[0].width = '1cm'
    legend_options_wid.children[1].children[1].children[2].children[0].children[
        0].children[1].width = '1cm'

    # align n_columns with spacing
    remove_class(legend_options_wid.children[1].children[1].children[2].children[0], 'vbox')
    add_class(legend_options_wid.children[1].children[1].children[2].children[0], 'hbox')

    # border around options
    if suboptions_border_visible:
        legend_options_wid.children[1].children[1].border = container_border

    # set toggle button font bold
    legend_options_wid.children[0].font_weight = toggle_button_font_weight

    # margin and border around container widget
    legend_options_wid.padding = container_padding
    legend_options_wid.margin = container_margin
    if border_visible:
        legend_options_wid.border = container_border


def update_legend_options(legend_options_wid, legend_options_dict):
    r"""
    Function that updates the state of a given font_options widget. Usage
    example:
        legend_options_default = {'render_legend':True,
                                  'legend_title':'',
                                  'legend_font_name':'serif',
                                  'legend_font_style':'normal',
                                  'legend_font_size':10,
                                  'legend_font_weight':'normal',
                                  'legend_marker_scale':1.,
                                  'legend_location':2,
                                  'legend_bbox_to_anchor':(1.05, 1.),
                                  'legend_border_axes_pad':1.,
                                  'legend_n_columns':1,
                                  'legend_horizontal_spacing':1.,
                                  'legend_vertical_spacing':1.,
                                  'legend_border':True,
                                  'legend_border_padding':0.5,
                                  'legend_shadow':False,
                                  'legend_rounded_corners':True}
        legend_options_wid = legend_options(legend_options_default)
        display(legend_options_wid)
        format_legend_options(legend_options_wid)
        legend_options_default = {'render_legend':True,
                                  'legend_title':'',
                                  'legend_font_name':'serif',
                                  'legend_font_style':'normal',
                                  'legend_font_size':10,
                                  'legend_font_weight':'normal',
                                  'legend_marker_scale':1.,
                                  'legend_location':2,
                                  'legend_bbox_to_anchor':(1.05, 1.),
                                  'legend_border_axes_pad':1.,
                                  'legend_n_columns':1,
                                  'legend_horizontal_spacing':1.,
                                  'legend_vertical_spacing':1.,
                                  'legend_border':True,
                                  'legend_border_padding':0.5,
                                  'legend_shadow':False,
                                  'legend_rounded_corners':True}
        update_legend_options(legend_options_wid, legend_options_dict)

    Parameters
    ----------
    legend_options_wid :
        The widget object generated by the `legend_options()` function.
    legend_options_dict : `dict`
        The new set of options. For example:
            legend_options_dict = {'render_legend':True,
                                   'legend_title':'',
                                   'legend_font_name':'serif',
                                   'legend_font_style':'normal',
                                   'legend_font_size':10,
                                   'legend_font_weight':'normal',
                                   'legend_marker_scale':1.,
                                   'legend_location':2,
                                   'legend_bbox_to_anchor':(1.05, 1.),
                                   'legend_border_axes_pad':1.,
                                   'legend_n_columns':1,
                                   'legend_horizontal_spacing':1.,
                                   'legend_vertical_spacing':1.,
                                   'legend_border':True,
                                   'legend_border_padding':0.5,
                                   'legend_shadow':False,
                                   'legend_rounded_corners':True}
    """
    # Assign new options dict to selected_values
    legend_options_wid.selected_values = legend_options_dict

    # update render legend checkbox
    if 'render_legend' in legend_options_dict.keys():
        legend_options_wid.children[1].children[0].value = \
            legend_options_dict['render_legend']

    # update legend_title
    if 'legend_title' in legend_options_dict.keys():
        legend_options_wid.children[1].children[1].children[1].children[0]. \
            value = legend_options_dict['legend_title']

    # update legend_font_name dropdown menu
    if 'legend_font_name' in legend_options_dict.keys():
        legend_options_wid.children[1].children[1].children[1].children[
            1].children[0].children[0].value = \
            legend_options_dict['legend_font_name']

    # update legend_font_size text box
    if 'legend_font_size' in legend_options_dict.keys():
        legend_options_wid.children[1].children[1].children[1].children[
            1].children[0].children[1].value = \
            int(legend_options_dict['legend_font_size'])

    # update legend_font_style dropdown menu
    if 'legend_font_style' in legend_options_dict.keys():
        legend_options_wid.children[1].children[1].children[1].children[
            1].children[1].children[0].value = \
            legend_options_dict['legend_font_style']

    # update legend_font_weight dropdown menu
    if 'legend_font_weight' in legend_options_dict.keys():
        legend_options_wid.children[1].children[1].children[1].children[
            1].children[1].children[1].value = \
            legend_options_dict['legend_font_weight']

    # update legend_location dropdown menu
    if 'legend_location' in legend_options_dict.keys():
        legend_options_wid.children[1].children[1].children[0].children[0]. \
            value = legend_options_dict['legend_location']

    # update legend_bbox_to_anchor
    if 'legend_bbox_to_anchor' in legend_options_dict.keys():
        if legend_options_dict['legend_bbox_to_anchor'] is None:
            tmp1 = False
            tmp2 = 0.
            tmp3 = 0.
        else:
            tmp1 = True
            tmp2 = legend_options_dict['legend_bbox_to_anchor'][0]
            tmp3 = legend_options_dict['legend_bbox_to_anchor'][1]
        legend_options_wid.children[1].children[1].children[0].children[
            1].children[0].value = tmp1
        legend_options_wid.children[1].children[1].children[0].children[
            1].children[1].value = tmp2
        legend_options_wid.children[1].children[1].children[0].children[
            1].children[2].value = tmp3

    # update legend_border_axes_pad
    if 'legend_border_axes_pad' in legend_options_dict.keys():
        legend_options_wid.children[1].children[1].children[0].children[
            2].value = \
            legend_options_dict['legend_border_axes_pad']

    # update legend_n_columns text box
    if 'legend_n_columns' in legend_options_dict.keys():
        legend_options_wid.children[1].children[1].children[2].children[
            0].children[0].children[0].value = \
            int(legend_options_dict['legend_n_columns'])

    # update legend_marker_scale text box
    if 'legend_marker_scale' in legend_options_dict.keys():
        legend_options_wid.children[1].children[1].children[2].children[
            0].children[0].children[1].value = \
            float(legend_options_dict['legend_marker_scale'])

    # update legend_horizontal_spacing text box
    if 'legend_horizontal_spacing' in legend_options_dict.keys():
        legend_options_wid.children[1].children[1].children[2].children[
            0].children[1].children[0].value = \
            float(legend_options_dict['legend_horizontal_spacing'])

    # update legend_vertical_spacing text box
    if 'legend_vertical_spacing' in legend_options_dict.keys():
        legend_options_wid.children[1].children[1].children[2].children[
            0].children[1].children[1].value = \
            float(legend_options_dict['legend_vertical_spacing'])

    # update legend_border
    if 'legend_border' in legend_options_dict.keys():
        legend_options_wid.children[1].children[1].children[2].children[
            1].children[0].value = \
            legend_options_dict['legend_border']

    # update legend_border_padding text box
    if 'legend_border_padding' in legend_options_dict.keys():
        legend_options_wid.children[1].children[1].children[2].children[
            1].children[1].value = \
            float(legend_options_dict['legend_border_padding'])

    # update legend_shadow
    if 'legend_shadow' in legend_options_dict.keys():
        legend_options_wid.children[1].children[1].children[2].children[
            2].children[0].value = \
            legend_options_dict['legend_shadow']

    # update legend_rounded_corners
    if 'legend_rounded_corners' in legend_options_dict.keys():
        legend_options_wid.children[1].children[1].children[2].children[
            2].children[1].value = \
            legend_options_dict['legend_rounded_corners']


def grid_options(grid_options_default, plot_function=None,
                 toggle_show_visible=True, toggle_show_default=True,
                 toggle_title='Grid Object', show_checkbox_title='Render grid'):
    r"""
    Creates a widget with Grid Options. Specifically, it has:
        1) A checkbox that controls grid's visibility.
        2) A dropdown menu for grid style.
        3) A bounded float text box for line width.
        7) A toggle button that controls the visibility of all the above, i.e.
           the grid options.

    The structure of the widgets is the following:
        grid_options_wid.children = [toggle_button, options]
        options.children = [render_grid_checkbox, other_options]
        other_options.children = [grid_style, grid_width]

    The returned widget saves the selected values in the following dictionary:
        grid_options_wid.selected_values

    To fix the alignment within this widget please refer to
    `format_grid_options()` function.

    Parameters
    ----------
    grid_options_default : `dict`
        The initial selected grid options.
        Example:
            line_options={'render_grid': True,
                          'grid_line_width': 1,
                          'grid_line_style': '-'}
    plot_function : `function` or None, optional
        The plot function that is executed when a widgets' value changes.
        If None, then nothing is assigned.
    toggle_show_default : `boolean`, optional
        Defines whether the options will be visible upon construction.
    toggle_show_visible : `boolean`, optional
        The visibility of the toggle button.
    toggle_title : `str`, optional
        The title of the toggle button.
    show_checkbox_title : `str`, optional
        The description of the show line checkbox.
    """
    import IPython.html.widgets as ipywidgets
    # Create widgets
    # toggle button
    but = ipywidgets.ToggleButton(description=toggle_title,
                                        value=toggle_show_default,
                                        visible=toggle_show_visible)

    # grid_line_style, grid_line_width
    render_grid = ipywidgets.Checkbox(
        description=show_checkbox_title,
        value=grid_options_default['render_grid'])
    grid_line_width = ipywidgets.BoundedFloatText(
        description='Width', value=grid_options_default['grid_line_width'],
        min=0.)
    grid_line_style_dict = OrderedDict()
    grid_line_style_dict['solid'] = '-'
    grid_line_style_dict['dashed'] = '--'
    grid_line_style_dict['dash-dot'] = '-.'
    grid_line_style_dict['dotted'] = ':'
    grid_line_style = ipywidgets.Dropdown(
        options=grid_line_style_dict,
        value=grid_options_default['grid_line_style'],
        description='Style')

    # Options widget
    all_grid_options = ipywidgets.Box(
        children=[grid_line_style, grid_line_width])
    options_wid = ipywidgets.Box(
        children=[render_grid, all_grid_options])

    # Final widget
    grid_options_wid = ipywidgets.Box(children=[but, options_wid])

    # Assign output
    grid_options_wid.selected_values = grid_options_default

    # line options visibility
    def options_visible(name, value):
        grid_line_style.disabled = not value
        grid_line_width.disabled = not value
    options_visible('', grid_options_default['render_grid'])
    render_grid.on_trait_change(options_visible, 'value')

    # get options functions
    def save_render_grid(name, value):
        grid_options_wid.selected_values['render_grid'] = value
    render_grid.on_trait_change(save_render_grid, 'value')

    def save_grid_line_width(name, value):
        grid_options_wid.selected_values['grid_line_width'] = float(value)
    grid_line_width.on_trait_change(save_grid_line_width, 'value')

    def save_grid_line_style(name, value):
        grid_options_wid.selected_values['grid_line_style'] = value
    grid_line_style.on_trait_change(save_grid_line_style, 'value')

    # Toggle button function
    def toggle_fun(name, value):
        options_wid.visible = value
    toggle_fun('', toggle_show_default)
    but.on_trait_change(toggle_fun, 'value')

    # assign plot_function
    if plot_function is not None:
        render_grid.on_trait_change(plot_function, 'value')
        grid_line_style.on_trait_change(plot_function, 'value')
        grid_line_width.on_trait_change(plot_function, 'value')

    return grid_options_wid


def format_grid_options(grid_options_wid, container_padding='6px',
                        container_margin='6px',
                        container_border='1px solid black',
                        toggle_button_font_weight='bold', border_visible=True,
                        suboptions_border_visible=True):
    r"""
    Function that corrects the align (style format) of a given grid_options
    widget. Usage example:
        grid_options_wid = grid_options()
        display(grid_options_wid)
        format_grid_options(grid_options_wid)

    Parameters
    ----------
    grid_options_wid :
        The widget object generated by the `grid_options()` function.
    container_padding : `str`, optional
        The padding around the widget, e.g. '6px'
    container_margin : `str`, optional
        The margin around the widget, e.g. '6px'
    container_border : `str`, optional
        The border around the widget, e.g. '1px solid black'
    toggle_button_font_weight : `str`
        The font weight of the toggle button, e.g. 'bold'
    border_visible : `boolean`, optional
        Defines whether to draw the border line around the widget.
    suboptions_border_visible : `boolean`, optional
        Defines whether to draw the border line around the line options, under
        the show line checkbox.
    """
    # align grid options with checkbox
    add_class(grid_options_wid.children[1], 'align-end')

    # set gridlinewidth text box width
    grid_options_wid.children[1].children[1].children[1].width = '1cm'

    # border around options
    if suboptions_border_visible:
        grid_options_wid.children[1].children[1].border = container_border

    # set toggle button font bold
    grid_options_wid.children[0].font_weight = toggle_button_font_weight

    # margin and border around container widget
    grid_options_wid.padding = container_padding
    grid_options_wid.margin = container_margin
    if border_visible:
        grid_options_wid.border = container_border


def update_grid_options(grid_options_wid, grid_options_dict):
    r"""
    Function that updates the state of a given grid_options widget. Usage
    example:
        default_grid_options={'render_grid':True,
                              'grid_line_width':2,
                              'grid_line_style':'-'}
        grid_options_wid = grid_options(default_grid_options)
        display(grid_options_wid)
        format_grid_options(grid_options_wid)
        default_grid_options={'render_grid':False,
                              'grid_line_width':4,
                              'grid_line_style':'-'}
        update_grid_options(grid_options_wid, default_grid_options)

    Parameters
    ----------
    grid_options_wid :
        The widget object generated by the `grid_options()` function.
    grid_options_dict : `dict`
        The new set of options. For example:
            grid_options_dict={'render_grid':True,
                               'grid_line_width':2,
                               'grid_line_style':'-'}
    """
    # Assign new options dict to selected_values
    grid_options_wid.selected_values = grid_options_dict

    # update render grid checkbox
    if 'render_grid' in grid_options_dict.keys():
        grid_options_wid.children[1].children[0].value = \
            grid_options_dict['render_grid']

    # update grid_line_style dropdown menu
    if 'grid_line_style' in grid_options_dict.keys():
        grid_options_wid.children[1].children[1].children[0].value = \
            grid_options_dict['grid_line_style']

    # update grid_line_width text box
    if 'grid_line_width' in grid_options_dict.keys():
        grid_options_wid.children[1].children[1].children[1].value = \
            float(grid_options_dict['grid_line_width'])


def hog_options(toggle_show_default=True, toggle_show_visible=True):
    r"""
    Creates a widget with HOG Features Options.

    The structure of the widgets is the following:
        hog_options_wid.children = [toggle_button, options]
        options.children = [window_wid, algorithm_wid]
        window_wid.children = [mode_wid, window_opts_wid]
        mode_wid.children = [mode_radiobuttons, padding_checkbox]
        window_opts_wid.children = [window_size_wid, window_step_wid]
        window_size_wid.children = [window_height, window_width,
                                    window_size_unit]
        window_step_wid.children = [window_vertical, window_horizontal,
                                    window_step_unit]
        algorithm_wid.children = [algorithm_radiobuttons, algorithm_options]
        algorithm_options.children = [algorithm_sizes, algorithm_other]
        algorithm_sizes.children = [cell_size, block_size, num_bins]
        algorithm_other.children = [signed_gradient, l2_norm_clipping]

    To fix the alignment within this widget please refer to
    `format_hog_options()` function.

    Parameters
    ----------
    toggle_show_default : `boolean`, optional
        Defines whether the options will be visible upon construction.
    toggle_show_visible : `boolean`, optional
        The visibility of the toggle button.
    """
    import IPython.html.widgets as ipywidgets
    # Toggle button that controls options' visibility
    but = ipywidgets.ToggleButton(description='HOG Options',
                                        value=toggle_show_default,
                                        visible=toggle_show_visible)

    # window related options
    tmp = OrderedDict()
    tmp['Dense'] = 'dense'
    tmp['Sparse'] = 'sparse'
    mode = ipywidgets.RadioButtons(options=tmp, description='Mode')
    padding = ipywidgets.Checkbox(value=True, description='Padding')
    mode_wid = ipywidgets.Box(children=[mode, padding])
    window_height = ipywidgets.BoundedIntText(value='1',
                                              description='Height', min=1)
    window_width = ipywidgets.BoundedIntText(value='1',
                                             description='Width', min=1)
    tmp = OrderedDict()
    tmp['Blocks'] = 'blocks'
    tmp['Pixels'] = 'pixels'
    window_size_unit = ipywidgets.RadioButtons(options=tmp,
                                               description=' Size unit')
    window_size_wid = ipywidgets.Box(
        children=[window_height, window_width,
                  window_size_unit])
    window_vertical = ipywidgets.BoundedIntText(value='1',
                                                description='Step Y',
                                                min=1)
    window_horizontal = ipywidgets.BoundedIntText(value='1',
                                                  description='Step X',
                                                  min=1)
    tmp = OrderedDict()
    tmp['Pixels'] = 'pixels'
    tmp['Cells'] = 'cells'
    window_step_unit = ipywidgets.RadioButtons(options=tmp,
                                               description='Step unit')
    window_step_wid = ipywidgets.Box(children=[window_vertical,
                                               window_horizontal,
                                               window_step_unit])
    window_wid = ipywidgets.Box(
        children=[window_size_wid, window_step_wid])
    window_wid = ipywidgets.Box(children=[mode_wid, window_wid])

    # algorithm related options
    tmp = OrderedDict()
    tmp['Dalal & Triggs'] = 'dalaltriggs'
    tmp['Zhu & Ramanan'] = 'zhuramanan'
    algorithm = ipywidgets.RadioButtons(options=tmp, value='dalaltriggs',
                                        description='Algorithm')
    cell_size = ipywidgets.BoundedIntText(
        value='8', description='Cell size (in pixels)', min=1)
    block_size = ipywidgets.BoundedIntText(
        value='2', description='Block size (in cells)', min=1)
    num_bins = ipywidgets.BoundedIntText(
        value='9', description='Orientation bins', min=1)
    algorithm_sizes = ipywidgets.Box(
        children=[cell_size, block_size,
                  num_bins])
    signed_gradient = ipywidgets.Checkbox(value=True,
                                          description='Signed gradients')
    l2_norm_clipping = ipywidgets.BoundedFloatText(
        value='0.2', description='L2 norm clipping', min=0.)
    algorithm_other = ipywidgets.Box(children=[signed_gradient,
                                               l2_norm_clipping])
    algorithm_options = ipywidgets.Box(children=[algorithm_sizes,
                                                 algorithm_other])
    algorithm_wid = ipywidgets.Box(
        children=[algorithm, algorithm_options])

    # options tab widget
    all_options = ipywidgets.Tab(children=[window_wid, algorithm_wid])

    # Widget container
    hog_options_wid = ipywidgets.Box(children=[but, all_options])

    # Initialize output dictionary
    hog_options_wid.options = {'mode': 'dense', 'algorithm': 'dalaltriggs',
                               'num_bins': 9, 'cell_size': 8, 'block_size': 2,
                               'signed_gradient': True, 'l2_norm_clip': 0.2,
                               'window_height': 1, 'window_width': 1,
                               'window_unit': 'blocks',
                               'window_step_vertical': 1,
                               'window_step_horizontal': 1,
                               'window_step_unit': 'pixels', 'padding': True,
                               'verbose': False}

    # mode function
    def window_mode(name, value):
        window_horizontal.disabled = value == 'sparse'
        window_vertical.disabled = value == 'sparse'
        window_step_unit.disabled = value == 'sparse'
        window_height.disabled = value == 'sparse'
        window_width.disabled = value == 'sparse'
        window_size_unit.disabled = value == 'sparse'
    mode.on_trait_change(window_mode, 'value')

    # algorithm function
    def algorithm_mode(name, value):
        l2_norm_clipping.disabled = value == 'zhuramanan'
        signed_gradient.disabled = value == 'zhuramanan'
        block_size.disabled = value == 'zhuramanan'
        num_bins.disabled = value == 'zhuramanan'
    algorithm.on_trait_change(algorithm_mode, 'value')

    # get options
    def get_mode(name, value):
        hog_options_wid.options['mode'] = value
    mode.on_trait_change(get_mode, 'value')

    def get_padding(name, value):
        hog_options_wid.options['padding'] = value
    padding.on_trait_change(get_padding, 'value')

    def get_window_height(name, value):
        hog_options_wid.options['window_height'] = value
    window_height.on_trait_change(get_window_height, 'value')

    def get_window_width(name, value):
        hog_options_wid.options['window_width'] = value
    window_width.on_trait_change(get_window_width, 'value')

    def get_window_size_unit(name, value):
        hog_options_wid.options['window_unit'] = value
    window_size_unit.on_trait_change(get_window_size_unit, 'value')

    def get_window_step_vertical(name, value):
        hog_options_wid.options['window_step_vertical'] = value
    window_vertical.on_trait_change(get_window_step_vertical, 'value')

    def get_window_step_horizontal(name, value):
        hog_options_wid.options['window_step_horizontal'] = value
    window_horizontal.on_trait_change(get_window_step_horizontal, 'value')

    def get_window_step_unit(name, value):
        hog_options_wid.options['window_step_unit'] = value
    window_step_unit.on_trait_change(get_window_step_unit, 'value')

    def get_algorithm(name, value):
        hog_options_wid.options['algorithm'] = value
    algorithm.on_trait_change(get_algorithm, 'value')

    def get_num_bins(name, value):
        hog_options_wid.options['num_bins'] = value
    num_bins.on_trait_change(get_num_bins, 'value')

    def get_cell_size(name, value):
        hog_options_wid.options['cell_size'] = value
    cell_size.on_trait_change(get_cell_size, 'value')

    def get_block_size(name, value):
        hog_options_wid.options['block_size'] = value
    block_size.on_trait_change(get_block_size, 'value')

    def get_signed_gradient(name, value):
        hog_options_wid.options['signed_gradient'] = value
    signed_gradient.on_trait_change(get_signed_gradient, 'value')

    def get_l2_norm_clip(name, value):
        hog_options_wid.options['l2_norm_clip'] = value
    l2_norm_clipping.on_trait_change(get_l2_norm_clip, 'value')

    # Toggle button function
    def toggle_options(name, value):
        all_options.visible = value
    but.on_trait_change(toggle_options, 'value')

    return hog_options_wid


def format_hog_options(hog_options_wid, container_padding='6px',
                       container_margin='6px',
                       container_border='1px solid black',
                       toggle_button_font_weight='bold',
                       border_visible=True):
    r"""
    Function that corrects the align (style format) of a given hog_options
    widget. Usage example:
        hog_options_wid = hog_options()
        display(hog_options_wid)
        format_hog_options(hog_options_wid)

    Parameters
    ----------
    hog_options_wid :
        The widget object generated by the `hog_options()` function.
    container_padding : `str`, optional
        The padding around the widget, e.g. '6px'
    container_margin : `str`, optional
        The margin around the widget, e.g. '6px'
    tab_top_margin : `str`, optional
        The margin around the tab options' widget, e.g. '0.3cm'
    container_border : `str`, optional
        The border around the widget, e.g. '1px solid black'
    toggle_button_font_weight : `str`
        The font weight of the toggle button, e.g. 'bold'
    border_visible : `boolean`, optional
        Defines whether to draw the border line around the widget.
    """
    # align window options
    remove_class(hog_options_wid.children[1].children[0].children[1], 'vbox')
    add_class(hog_options_wid.children[1].children[0].children[1], 'hbox')

    # set width of height, width, step x , step y textboxes
    hog_options_wid.children[1].children[0].children[1].children[0].children[0]. \
        width = '40px'
    hog_options_wid.children[1].children[0].children[1].children[0].children[1]. \
        width = '40px'
    hog_options_wid.children[1].children[0].children[1].children[1].children[0]. \
        width = '40px'
    hog_options_wid.children[1].children[0].children[1].children[1].children[1]. \
        width = '40px'

    # set margin and border around the window size and step options
    hog_options_wid.children[1].children[0].children[1].children[0]. \
        margin = container_margin
    hog_options_wid.children[1].children[0].children[1].children[1]. \
        margin = container_margin
    hog_options_wid.children[1].children[0].children[1].children[0]. \
        border = '1px solid gray'
    hog_options_wid.children[1].children[0].children[1].children[1]. \
        border = '1px solid gray'

    # align mode and padding
    remove_class(hog_options_wid.children[1].children[0].children[0], 'vbox')
    add_class(hog_options_wid.children[1].children[0].children[0], 'hbox')

    # set width of algorithm textboxes
    hog_options_wid.children[1].children[1].children[1].children[0].children[0]. \
        width = '40px'
    hog_options_wid.children[1].children[1].children[1].children[0].children[1]. \
        width = '40px'
    hog_options_wid.children[1].children[1].children[1].children[0].children[2]. \
        width = '40px'
    hog_options_wid.children[1].children[1].children[1].children[1].children[1]. \
        width = '40px'

    # align algorithm options
    remove_class(hog_options_wid.children[1].children[1].children[1], 'vbox')
    add_class(hog_options_wid.children[1].children[1].children[1], 'hbox')

    # set margin and border around the algorithm options
    hog_options_wid.children[1].children[1].children[1]. \
        margin = container_margin
    hog_options_wid.children[1].children[1].children[1]. \
        border = '1px solid gray'

    hog_options_wid.children[1].margin_top = '6px'
    add_class(hog_options_wid.children[1].children[0], 'align-center')
    add_class(hog_options_wid.children[1].children[1], 'align-center')

    # set final tab titles
    tab_titles = ['Window', 'Algorithm']
    for (k, tl) in enumerate(tab_titles):
        hog_options_wid.children[1].set_title(k, tl)

    # set toggle button font bold
    hog_options_wid.children[0].font_weight = toggle_button_font_weight

    # margin and border around container widget
    hog_options_wid.padding = container_padding
    hog_options_wid.margin = container_margin
    if border_visible:
        hog_options_wid.border = container_border


def daisy_options(toggle_show_default=True, toggle_show_visible=True):
    r"""
    Creates a widget with Daisy Features Options.

    The structure of the widgets is the following:
        daisy_options_wid.children = [toggle_button, options]
        options.children = [options1, options2]
        options1.children = [step_int, radius_int, rings_int, histograms_int]
        options2.children = [orientations_int, normalization_dropdown,
                             sigmas_list, ring_radii_list]

    To fix the alignment within this widget please refer to
    `format_daisy_options()` function.

    Parameters
    ----------
    toggle_show_default : `boolean`, optional
        Defines whether the options will be visible upon construction.
    toggle_show_visible : `boolean`, optional
        The visibility of the toggle button.
    """
    import IPython.html.widgets as ipywidgets
    # Toggle button that controls options' visibility
    but = ipywidgets.ToggleButton(description='Daisy Options',
                                  value=toggle_show_default,
                                  visible=toggle_show_visible)

    # options widgets
    step = ipywidgets.BoundedIntText(value='1', description='Step', min=1)
    radius = ipywidgets.BoundedIntText(value='15', description='Radius',
                                       min=1)
    rings = ipywidgets.BoundedIntText(value='2', description='Rings',
                                      min=1)
    histograms = ipywidgets.BoundedIntText(value='2',
                                           description='Histograms',
                                           min=1)
    orientations = ipywidgets.BoundedIntText(value='8',
                                             description='Orientations',
                                             min=1)
    tmp = OrderedDict()
    tmp['L1'] = 'l1'
    tmp['L2'] = 'l2'
    tmp['Daisy'] = 'daisy'
    tmp['None'] = None
    normalization = ipywidgets.Dropdown(value='l1', options=tmp,
                                        description='Normalization')
    sigmas = ipywidgets.Text(description='Sigmas')
    ring_radii = ipywidgets.Text(description='Ring radii')

    # group widgets
    cont1 = ipywidgets.Box(
        children=[step, radius, rings, histograms])
    cont2 = ipywidgets.Box(
        children=[orientations, normalization, sigmas,
                  ring_radii])
    options = ipywidgets.Box(children=[cont1, cont2])

    # Widget container
    daisy_options_wid = ipywidgets.Box(children=[but, options])

    # Initialize output dictionary
    daisy_options_wid.options = {'step': 1, 'radius': 15,
                                 'rings': 2, 'histograms': 2,
                                 'orientations': 8,
                                 'normalization': 'l1',
                                 'sigmas': None,
                                 'ring_radii': None}

    # get options
    def get_step(name, value):
        daisy_options_wid.options['step'] = value

    step.on_trait_change(get_step, 'value')

    def get_radius(name, value):
        daisy_options_wid.options['radius'] = value

    radius.on_trait_change(get_radius, 'value')

    def get_rings(name, value):
        daisy_options_wid.options['rings'] = value

    rings.on_trait_change(get_rings, 'value')

    def get_histograms(name, value):
        daisy_options_wid.options['histograms'] = value

    histograms.on_trait_change(get_histograms, 'value')

    def get_orientations(name, value):
        daisy_options_wid.options['orientations'] = value

    orientations.on_trait_change(get_orientations, 'value')

    def get_normalization(name, value):
        daisy_options_wid.options['normalization'] = value

    normalization.on_trait_change(get_normalization, 'value')

    def get_sigmas(name, value):
        daisy_options_wid.options['sigmas'] = _convert_str_to_list_int(
            str(value))

    sigmas.on_trait_change(get_sigmas, 'value')

    def get_ring_radii(name, value):
        daisy_options_wid.options['ring_radii'] = _convert_str_to_list_float(
            str(value))

    ring_radii.on_trait_change(get_ring_radii, 'value')

    # Toggle button function
    def toggle_options(name, value):
        options.visible = value

    but.on_trait_change(toggle_options, 'value')

    return daisy_options_wid


def format_daisy_options(daisy_options_wid, container_padding='6px',
                         container_margin='6px',
                         container_border='1px solid black',
                         toggle_button_font_weight='bold',
                         border_visible=True):
    r"""
    Function that corrects the align (style format) of a given daisy_options
    widget. Usage example:
        daisy_options_wid = daisy_options()
        display(daisy_options_wid)
        format_daisy_options(daisy_options_wid)

    Parameters
    ----------
    daisy_options_wid :
        The widget object generated by the `daisy_options()` function.
    container_padding : `str`, optional
        The padding around the widget, e.g. '6px'
    container_margin : `str`, optional
        The margin around the widget, e.g. '6px'
    tab_top_margin : `str`, optional
        The margin around the tab options' widget, e.g. '0.3cm'
    container_border : `str`, optional
        The border around the widget, e.g. '1px solid black'
    toggle_button_font_weight : `str`
        The font weight of the toggle button, e.g. 'bold'
    border_visible : `boolean`, optional
        Defines whether to draw the border line around the widget.
    """
    # align window options
    daisy_options_wid.children[1]._dom_classes.remove('vbox')
    daisy_options_wid.children[1]._dom_classes.append('hbox')

    # set textboxes length
    daisy_options_wid.children[1].children[0].children[0].width = '40px'
    daisy_options_wid.children[1].children[0].children[1].width = '40px'
    daisy_options_wid.children[1].children[0].children[2].width = '40px'
    daisy_options_wid.children[1].children[0].children[3].width = '40px'
    daisy_options_wid.children[1].children[1].children[0].width = '40px'
    daisy_options_wid.children[1].children[1].children[2].width = '80px'
    daisy_options_wid.children[1].children[1].children[3].width = '80px'

    # set toggle button font bold
    daisy_options_wid.children[0].font_weight = toggle_button_font_weight

    # margin and border around container widget
    daisy_options_wid.padding = container_padding
    daisy_options_wid.margin = container_margin
    if border_visible:
        daisy_options_wid.border = container_border


def lbp_options(toggle_show_default=True, toggle_show_visible=True):
    r"""
    Creates a widget with LBP Features Options.

    The structure of the widgets is the following:
        lbp_options_wid.children = [toggle_button, options]
        options.children = [window_wid, algorithm_wid]
        window_wid.children = [window_vertical, window_horizontal,
                               window_step_unit, padding]
        algorithm_wid.children = [mapping_type, radius, samples]

    To fix the alignment within this widget please refer to
    `format_lbp_options()` function.

    Parameters
    ----------
    toggle_show_default : `boolean`, optional
        Defines whether the options will be visible upon construction.
    toggle_show_visible : `boolean`, optional
        The visibility of the toggle button.
    """
    import IPython.html.widgets as ipywidgets
    # Toggle button that controls options' visibility
    but = ipywidgets.ToggleButton(description='LBP Options',
                                        value=toggle_show_default,
                                        visible=toggle_show_visible)

    # method related options
    tmp = OrderedDict()
    tmp['Uniform-2'] = 'u2'
    tmp['Rotation-Invariant'] = 'ri'
    tmp['Both'] = 'riu2'
    tmp['None'] = 'none'
    mapping_type = ipywidgets.Dropdown(value='u2', options=tmp,
                                       description='Mapping')
    radius = ipywidgets.Text(value='1, 2, 3, 4', description='Radius')
    samples = ipywidgets.Text(value='8, 8, 8, 8', description='Samples')
    algorithm_wid = ipywidgets.Box(children=[radius, samples, mapping_type])

    # window related options
    window_vertical = ipywidgets.BoundedIntText(value='1',
                                                      description='Step Y',
                                                      min=1)
    window_horizontal = ipywidgets.BoundedIntText(value='1',
                                                        description='Step X',
                                                        min=1)
    tmp = OrderedDict()
    tmp['Pixels'] = 'pixels'
    tmp['Windows'] = 'cells'
    window_step_unit = ipywidgets.RadioButtons(options=tmp,
                                               description='Step unit')
    padding = ipywidgets.Checkbox(value=True, description='Padding')
    window_wid = ipywidgets.Box(children=[window_vertical, window_horizontal,
                                          window_step_unit, padding])

    # options widget
    options = ipywidgets.Box(children=[window_wid, algorithm_wid])

    # Widget container
    lbp_options_wid = ipywidgets.Box(children=[but, options])

    # Initialize output dictionary
    lbp_options_wid.options = {'radius': range(1, 5), 'samples': [8] * 4,
                               'mapping_type': 'u2',
                               'window_step_vertical': 1,
                               'window_step_horizontal': 1,
                               'window_step_unit': 'pixels', 'padding': True,
                               'verbose': False, 'skip_checks': False}

    # get options
    def get_mapping_type(name, value):
        lbp_options_wid.options['mapping_type'] = value
    mapping_type.on_trait_change(get_mapping_type, 'value')

    def get_window_vertical(name, value):
        lbp_options_wid.options['window_step_vertical'] = value
    window_vertical.on_trait_change(get_window_vertical, 'value')

    def get_window_horizontal(name, value):
        lbp_options_wid.options['window_step_horizontal'] = value
    window_horizontal.on_trait_change(get_window_horizontal, 'value')

    def get_window_step_unit(name, value):
        lbp_options_wid.options['window_step_unit'] = value
    window_step_unit.on_trait_change(get_window_step_unit, 'value')

    def get_padding(name, value):
        lbp_options_wid.options['padding'] = value
    padding.on_trait_change(get_padding, 'value')

    def get_radius(name, value):
        lbp_options_wid.options['radius'] = _convert_str_to_list_int(str(value))
    radius.on_trait_change(get_radius, 'value')

    def get_samples(name, value):
        str_val = _convert_str_to_list_int(str(value))
        lbp_options_wid.options['samples'] = str_val
    samples.on_trait_change(get_samples, 'value')

    # Toggle button function
    def toggle_options(name, value):
        options.visible = value
    but.on_trait_change(toggle_options, 'value')

    return lbp_options_wid


def format_lbp_options(lbp_options_wid, container_padding='6px',
                       container_margin='6px',
                       container_border='1px solid black',
                       toggle_button_font_weight='bold',
                       border_visible=True):
    r"""
    Function that corrects the align (style format) of a given lbp_options
    widget. Usage example:
        lbp_options_wid = lbp_options()
        display(lbp_options_wid)
        format_lbp_options(lbp_options_wid)

    Parameters
    ----------
    lbp_options_wid :
        The widget object generated by the `lbp_options()` function.
    container_padding : `str`, optional
        The padding around the widget, e.g. '6px'
    container_margin : `str`, optional
        The margin around the widget, e.g. '6px'
    tab_top_margin : `str`, optional
        The margin around the tab options' widget, e.g. '0.3cm'
    container_border : `str`, optional
        The border around the widget, e.g. '1px solid black'
    toggle_button_font_weight : `str`
        The font weight of the toggle button, e.g. 'bold'
    border_visible : `boolean`, optional
        Defines whether to draw the border line around the widget.
    """
    # align window options
    remove_class(lbp_options_wid.children[1], 'vbox')
    add_class(lbp_options_wid.children[1], 'hbox')

    # set textboxes length
    lbp_options_wid.children[1].children[0].children[0].width = '40px'
    lbp_options_wid.children[1].children[0].children[1].width = '40px'
    lbp_options_wid.children[1].children[1].children[0].width = '80px'
    lbp_options_wid.children[1].children[1].children[1].width = '80px'

    # set toggle button font bold
    lbp_options_wid.children[0].font_weight = toggle_button_font_weight

    # margin and border around container widget
    lbp_options_wid.padding = container_padding
    lbp_options_wid.margin = container_margin
    if border_visible:
        lbp_options_wid.border = container_border


def igo_options(toggle_show_default=True, toggle_show_visible=True):
    r"""
    Creates a widget with IGO Features Options.

    The structure of the widgets is the following:
        igo_options_wid.children = [toggle_button, double_angles_checkbox]

    To fix the alignment within this widget please refer to
    `format_igo_options()` function.

    Parameters
    ----------
    toggle_show_default : `boolean`, optional
        Defines whether the options will be visible upon construction.
    toggle_show_visible : `boolean`, optional
        The visibility of the toggle button.
    """
    import IPython.html.widgets as ipywidgets
    # Toggle button that controls options' visibility
    but = ipywidgets.ToggleButton(description='IGO Options',
                                        value=toggle_show_default,
                                        visible=toggle_show_visible)

    # options widget
    double_angles = ipywidgets.Checkbox(value=False,
                                              description='Double angles')

    # Widget container
    igo_options_wid = ipywidgets.Box(children=[but, double_angles])

    # Initialize output dictionary
    igo_options_wid.options = {'double_angles': False}

    # get double_angles
    def get_double_angles(name, value):
        igo_options_wid.options['double_angles'] = value
    double_angles.on_trait_change(get_double_angles, 'value')

    # Toggle button function
    def toggle_options(name, value):
        double_angles.visible = value
    but.on_trait_change(toggle_options, 'value')

    return igo_options_wid


def format_igo_options(igo_options_wid, container_padding='6px',
                       container_margin='6px',
                       container_border='1px solid black',
                       toggle_button_font_weight='bold',
                       border_visible=True):
    r"""
    Function that corrects the align (style format) of a given igo_options
    widget. Usage example:
        igo_options_wid = igo_options()
        display(igo_options_wid)
        format_igo_options(igo_options_wid)

    Parameters
    ----------
    igo_options_wid :
        The widget object generated by the `igo_options()` function.
    container_padding : `str`, optional
        The padding around the widget, e.g. '6px'
    container_margin : `str`, optional
        The margin around the widget, e.g. '6px'
    tab_top_margin : `str`, optional
        The margin around the tab options' widget, e.g. '0.3cm'
    container_border : `str`, optional
        The border around the widget, e.g. '1px solid black'
    toggle_button_font_weight : `str`
        The font weight of the toggle button, e.g. 'bold'
    border_visible : `boolean`, optional
        Defines whether to draw the border line around the widget.
    """
    # set toggle button font bold
    igo_options_wid.children[0].font_weight = toggle_button_font_weight

    # margin and border around container widget
    igo_options_wid.padding = container_padding
    igo_options_wid.margin = container_margin
    if border_visible:
        igo_options_wid.border = container_border


def function_definition(default_function='def my_function():\n    pass',
                        toggle_show_default=True, toggle_show_visible=True):
    r"""
    Creates a widget for Function Definition.

    The structure of the widgets is the following:
        function_definition_wid.children = [toggle_button, options]
        options.children = [code_textarea, define]
        define.children = [message_text, define_button]

    To fix the alignment within this widget please refer to
    `format_function_definition()` function.

    Parameters
    ----------
    toggle_show_default : `boolean`, optional
        Defines whether the options will be visible upon construction.
    toggle_show_visible : `boolean`, optional
        The visibility of the toggle button.
    """
    import IPython.html.widgets as ipywidgets
    # Toggle button that controls options' visibility
    but = ipywidgets.ToggleButton(description='Features Options',
                                        value=toggle_show_default,
                                        visible=toggle_show_visible)

    # code widget
    code = ipywidgets.Textarea(value=default_function)
    define_but = ipywidgets.Button(description='Define')
    msg_wid = ipywidgets.Latex(value='')
    define_wid = ipywidgets.Box(children=[msg_wid, define_but])

    # options widget
    all_options = ipywidgets.Box(children=[code, define_wid])

    # Widget container
    function_definition_wid = ipywidgets.Box(
        children=[but, all_options])

    # Initialize output dictionary
    f, msg = _get_function_handle_from_string(default_function)
    function_definition_wid.function = f

    # get code
    def get_code(name):
        function_handle, msg = _get_function_handle_from_string(code.value)
        if function_handle is not None:
            function_definition_wid.function = function_handle
            msg_wid.value = ''
        else:
            f, _ = _get_function_handle_from_string(default_function)
            function_definition_wid.function = f
            msg_wid.value = msg
    define_but.on_click(get_code)

    # Toggle button function
    def toggle_options(name, value):
        all_options.visible = value
    but.on_trait_change(toggle_options, 'value')

    return function_definition_wid


def format_function_definition(function_definition_wid, container_padding='6px',
                               container_margin='6px',
                               container_border='1px solid black',
                               toggle_button_font_weight='bold',
                               border_visible=True):
    r"""
    Function that corrects the align (style format) of a given features_options
    widget. Usage example:
        function_definition_wid = function_definition()
        display(function_definition_wid)
        format_function_definition(function_definition_wid)

    Parameters
    ----------
    function_definition_wid :
        The widget object generated by the `function_definition()` function.
    container_padding : `str`, optional
        The padding around the widget, e.g. '6px'
    container_margin : `str`, optional
        The margin around the widget, e.g. '6px'
    tab_top_margin : `str`, optional
        The margin around the tab options' widget, e.g. '0.3cm'
    container_border : `str`, optional
        The border around the widget, e.g. '1px solid black'
    toggle_button_font_weight : `str`
        The font weight of the toggle button, e.g. 'bold'
    border_visible : `boolean`, optional
        Defines whether to draw the border line around the widget.
    """
    # align message text and button horizontally
    remove_class(function_definition_wid.children[1].children[1], 'vbox')
    add_class(function_definition_wid.children[1].children[1], 'hbox')

    # set margin between message and button
    function_definition_wid.children[1].children[1].children[0].margin_right = '0.5cm'

    # align code textarea and button to the right
    add_class(function_definition_wid.children[1], 'align-end')

    # set error message background to red
    function_definition_wid.children[1].children[1].children[0].background = 'red'

    # set toggle button font bold
    function_definition_wid.children[0].font_weight = toggle_button_font_weight

    # margin and border around container widget
    function_definition_wid.padding = container_padding
    function_definition_wid.margin = container_margin
    if border_visible:
        function_definition_wid.border = container_border


class IntListText():
    r"""
    Basic widget that returns a `list` of `int` numbers. It uses
    `IPython.html.widgets.Text()` and converts its value to a `list` of
    `int`.

    Parameters
    ----------
    value : `str` or `list` of `int`, Optional
        The initial value of the widget.
    description : `str`, Optional
        The description of the widget.

    Raises
    ------
    ValueError
        value must be str or list
    """

    def __init__(self, value='', description=''):
        import IPython.html.widgets as ipywidgets

        if isinstance(value, list):
            val = _convert_list_to_str(value)
        elif isinstance(value, str):
            val = value
        else:
            raise ValueError("value must be str or list")
        self.text_wid = ipywidgets.Text(value=val,
                                              description=description)

    @property
    def value(self):
        r"""
        The value fo the widget.
        """
        return _convert_str_to_list_int(str(self.text_wid.value))

    @property
    def description(self):
        r"""
        The description of the widget.
        """
        return self.text_wid.description

    @property
    def model_id(self):
        r"""
        The id of the widget.
        """
        return self.text_wid.model_id


class FloatListText(IntListText):
    r"""
    Basic widget that returns a `list` of `float` numbers. It uses
    `IPython.html.widgets.Text()` and converts its value to a `list` of
    `float`.

    Parameters
    ----------
    value : `str` or `list` of `int`, Optional
        The initial value of the widget.
    description : `str`, Optional
        The description of the widget.

    Raises
    ------
    ValueError
        value must be str or list
    """

    @property
    def value(self):
        r"""
        The value fo the widget.
        """
        return _convert_str_to_list_float(str(self.text_wid.value))


def _convert_list_to_str(l):
    r"""
    Function that converts a given list of numbers to a string. For example:
        convert_list_to_str([1, 2, 3]) returns '1, 2, 3'
    """
    if isinstance(l, list):
        return str(l)[1:-1]
    else:
        return ''


def _convert_str_to_list_int(s):
    r"""
    Function that converts a given string to a list of int numbers. For example:
        _convert_str_to_list_int('1, 2, 3') returns [1, 2, 3]
    """
    if isinstance(s, str):
        return [int(i[:-1]) if i[-1] == ',' else int(i) for i in s.split()]
    else:
        return []


def _convert_str_to_list_float(s):
    r"""
    Function that converts a given string to a list of float numbers.
    For example:
        _convert_str_to_list_float('1, 2, 3') returns [1.0, 2.0, 3.0]
    """
    if isinstance(s, str):
        return [float(i[:-1]) if i[-1] == ',' else float(i) for i in s.split()]
    else:
        return []


def _get_function_handle_from_string(s):
    r"""
    Function that returns a function handle given the function code as a string.
    """
    try:
        exec(s)
        function_name = s[4:s.find('(')]
        return eval(function_name), None
    except:
        return None, 'Invalid syntax!'


def _convert_image_to_bytes(image):
    r"""
    Function that given a menpo.Image object, it converts it to the correct
    bytes format that can be used by IPython.html.widgets.Image().
    """
    fp = StringIO()
    image.as_PILImage().save(fp, format='png')
    fp.seek(0)
    return fp.read()


def _lists_are_the_same(a, b):
    if len(a) == len(b):
        for i, j in zip(a, b):
            if i != j:
                return False
        return True
    else:
        return False

