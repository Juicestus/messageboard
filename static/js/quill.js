/*
 * Quill Interface Code
 * (c) Justus Languell 2020-2021
 */

var toolbarOptions = [];

// Inst. Quill
function getQuillE()
{
    var q = new Quill('.editor', 
	{
		theme: 'bubble',
        modules: {
            toolbar: toolbarOptions
        },
        placeholder: 'Message. You can paste images here or use the file upload. Limit 1 image for testing.'
	});
    return q;
};

// Parses Input
function parseDelta(delta)
{
    var ops = delta.ops;
    var text = '';

    b64img = 'NOIMAGE';
    webimg = 'NOIMAGE';


    for (var i=0; i<ops.length; i++)
    {
        var insert = ops[i].insert;
        
        if (typeof insert == 'object') 
        {
            if ((webimg == 'NOIMAGE') && (b64img == 'NOIMAGE'))
            {
                if (insert.image.substring(0,11) == 'data:image/')
                {
                    b64img = insert.image;
                }
                else
                {          
                    webimg = insert.image;         
                };
            };
        }
        else 
        {
            text += insert;
        };
    };
    return [text, b64img, webimg];
};

// Clears Box
function qClear(q)
{
    q.setContents([{ insert: '' }]);
};

