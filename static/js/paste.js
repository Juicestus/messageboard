/*
 * Handles pasting of images
 * (c) Justus Languell w/ *strong inspiration* 
 *     from a much better JS dev (;
 */

var PasteImage = function (el) 
{
    this._el = el;
    this._listenForPaste();
};

PasteImage.prototype._getURLObj = function () 
{
    return window.URL || window.webkitURL;
};

PasteImage.prototype._pasteImage = function (image) 
{
    this.emit('paste-image', image);
};

PasteImage.prototype._pasteImageSource = function (src) 
{
    var self = this,
        image = new Image();

    image.onload = function () 
    {
        self._pasteImage(image);
    };

    image.src = src;
};

PasteImage.prototype._pasteImageSource = function (src) 
{
    this.emit('paste-text', text);
};

PasteImage.prototype._onPaste = function (e) 
{

    // We need to check if event.clipboardData is supported (Chrome & IE)
    if (e.clipboardData && e.clipboardData.items) 
    {
        e.preventDefault();

        // Get the items from the clipboard
        var items = e.clipboardData.items;

        // Loop through all items, looking for any kind of image
        for (var i = 0; i < items.length; i++) 
        {
            if (items[i].type.indexOf('image') !== -1) 
            {
                // We need to represent the image as a file
                var blob = items[i].getAsFile();

                // Use a URL or webkitURL (whichever is available to the browser) to create a
                // temporary URL to the object
                var URLObj = this._getURLObj();
                var source = URLObj.createObjectURL(blob);

                // The URL can then be used as the source of an image
                this._pasteImageSource(source);

                // Prevent the image (or URL) from being pasted into the contenteditable element
                //e.preventDefault();
            }
            else
            {
                items[i].getAsString(function (s)
                {
                    //this._pasteText(extractContent(s));

                    pastetext(extractContent(s));
                    //e.preventDefault();
                });
            }
        }
    }
};

PasteImage.prototype._listenForPaste = function () 
{
    var self = this;

    self._origOnPaste = self._el.onpaste;

    self._el.addEventListener('paste', function (e) 
    {

        self._onPaste(e);

        // Preserve an existing onpaste event handler
        if (self._origOnPaste) 
        {
            self._origOnPaste.apply(this, arguments);
        }

    });
};

PasteImage.prototype.on = function (event, callback) 
{
    this._callback = callback;
};

PasteImage.prototype.emit = function (event, arg)
{
    this._callback(arg);
};


var pasteImage = new PasteImage(document.getElementById('messageArea'));

pasteImage.on('paste-image', function (image)
{

    if (image.nodeName == 'IMG')
    {
        src = image.getAttribute("src");
        image.setAttribute("class", "pastin");


        var childs = document.getElementById('messageArea').children


        console.log(childs)

        var count = 0;
        for (var i = 0; i < childs.length; ++i)
        {
            if (childs[i].nodeName == 'IMG')
            {
                count++;
            }
        }
        
        console.log(count)

        if (count < 1)
        {
            document.getElementById('messageArea').innerHTML += `<img class="pastin" src="${src}">`;
        }
        
    }

});

function pastetext(text)
{
    console.log(text)
    document.getElementById('messageArea').innerHTML += `${text}`;
}
// Rework this entire system to plaintextify evereything!
// And just format better ig...