import React from "react";
import {useParams} from "react-router-dom";



const BookItem = ({book,authors}) => {

      return (
        <tr>
            <td>
                {book.id}
            </td>
            <td>
                {book.name}
            </td>
            <td>
                {book.authors.map((authorId) =>{
                    let author = authors.find((author) => author.id === authorId )
                    if(author){
                        return author.last_name}
                })}
            </td>
        </tr>
    )

}

const BookListAuthors = ({books,authors}) => {

    let {id} = useParams()
    console.log()

    let filter_item = books.filter((book => book.authors.includes(parseInt(id))))

    return(
        <table>
            <th>
                ID
            </th>
               <th>
                Name
            </th>
               <th>
                Author
            </th>
            {filter_item.map((book) => <BookItem book={book} authors={authors}/> )}
        </table>
    )

}

export default BookListAuthors