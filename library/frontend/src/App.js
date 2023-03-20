import React from 'react';
import axios from 'axios';
import logo from './logo.svg';
import './App.css';
import AuthorList from "./components/Author.js";
import BookList from "./components/Book.js";
import NotFound404 from "./components/NotFound404.js";
import BookListAuthors from "./components/BooksAuthor.js";
import {HashRouter,Route,BrowserRouter,Link,Switch,Redirect} from "react-router-dom";


class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            'authors': [],
            'books':[]
        }
    }

    componentDidMount() {
        axios.get('http://127.0.0.1:8000/api/authors/').then(response => {
            this.setState(
                {
                    'authors': response.data
                }
            )}).catch(error => console.log(error))

        axios.get('http://127.0.0.1:8000/api/books/').then(response => {
            this.setState(
                {
                    'books': response.data
                }
            )}).catch(error => console.log(error))

    }

    render() {
        return (
            <div>
                <BrowserRouter>
                    <nav>
                        <ul>
                            <li>
                                <Link to='/'> Authors</Link>
                            </li>
                            <li>
                                <Link to='/books'>Books</Link>
                            </li>
                        </ul>
                    </nav>

                    <Switch>
                        <Route exact path='/' component={() => <AuthorList authors={this.state.authors}/>}/>
                        <Route exact path='/books' component={() =>  <BookList books={this.state.books}/>}/>

                        <Route path='/author/:id'>
                            <BookListAuthors books={this.state.books}  authors={this.state.authors}/>
                        </Route>

                        <Redirect from='/book' to='/books'/>
                        <Route component={NotFound404}/>
                     </Switch>
                </BrowserRouter>
            </div>
        );
    }
}

export default App;
