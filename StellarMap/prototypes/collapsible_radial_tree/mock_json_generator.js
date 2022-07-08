// https://json-generator.com/
{
name: '{{lorem(1, "words")}}',
full_id: '{{objectId().toUpperCase()}}',
description: '{{lorem(3, "words")}}',
url: '{{random("google.co", "yahoo.com", "qwant.com")}}',
created: '{{date(new Date(2014, 0, 1), new Date(), "YYYY-MM-ddThh:mm:ss Z")}}',
children: [
        '{{repeat(3, 9)}}',
        {
        name: '{{lorem(1, "words")}}',
        full_id: '{{objectId().toUpperCase()}}',
        description: '{{lorem(6, "words")}}',
        url: '{{random("google.co", "yahoo.com", "qwant.com")}}',
        created: '{{date(new Date(2014, 0, 1), new Date(), "YYYY-MM-ddThh:mm:ss Z")}}',
        children: [
            '{{repeat(9, 17)}}',
            {
            name: '{{lorem(1, "words")}}',
            full_id: '{{objectId().toUpperCase()}}',
            description: '{{lorem(3, "words")}}',
            url: '{{random("google.co", "yahoo.com", "qwant.com")}}',
            created: '{{date(new Date(2014, 0, 1), new Date(), "YYYY-MM-ddThh:mm:ss Z")}}',
            children: [
                '{{repeat(0, 3)}}',
                {
                name: '{{lorem(1, "words")}}',
                full_id: '{{objectId().toUpperCase()}}',
                description: '{{lorem(17, "words")}}',
                url: '{{random("google.co", "yahoo.com", "qwant.com")}}',
                created: '{{date(new Date(2014, 0, 1), new Date(), "YYYY-MM-ddThh:mm:ss Z")}}'
                }
            ]
            }
        ]
        }	
    ]
}
