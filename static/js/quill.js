/*
 * Quill Interface Code
 * (c) Justus Languell 2020-2021
 */

var tagl = '0xB1eDA5F757CF381d66dBd4ab867e69d217415759_L';
var tagr = '0xB1eDA5F757CF381d66dBd4ab867e69d217415759_R';

function getQuillE()
{
    var q = new Quill('.editor', 
	{
		theme: 'bubble',
        placeholder: 'Try pasting an image from Google! For downloaded images, continue to use the uplaod for now'
		//placeholder: 'Message...'
	});
    return q;
}

function parseDelta(delta)
{
    var ops = delta.ops;
    var text = '';

    for (var i=0; i<ops.length; i++)
    {
        var insert = ops[i].insert;
        
        if (typeof insert == 'object') 
        {
            text += `${tagl}img src="${insert.image}"${tagr}`;
        }
        else 
        {
            text += insert;
        }
    }
    return text;
}

function qClear(q)
{
    q.setContents([{ insert: '' }]);
}