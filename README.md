***Words Search***

This application provides an API to get suggested relevant words based on below criteria:
> Exact match should be first

> If search term is present in the beginning of a word it will be ranked higher

> Words with higher frequency are given preference

> Short words are given preference over long words 

Application has below endpoint:

> /search?word=`input`

where, `input`=user input (word to be searched)
    
Above API returns JSON Array up to 25 results based on ranking
