import React from 'react';
import axios from 'axios';
import logo from './logo.svg';
import './App.css';
import AuthorList from "./components/Author.js";
import BookList from "./components/Book.js";
import NotFound404 from "./components/NotFound404.js";
import BookListAuthors from "./components/BooksAuthor.js";
import LoginForm from "./components/Auth.js";
import {HashRouter, Route, BrowserRouter, Link, Switch, Redirect} from "react-router-dom";
import Cookies from "universal-cookie";

class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            'authors': [],
            'books': [],
            'token': ''
        }
    }

    load_data() {
        const headers = this.get_headers()
        axios.get('http://127.0.0.1:8005/api/authors/',{headers}).then(response => {
            this.setState(
                {
                    'authors': response.data
                }
            )
        }).catch(error => console.log(error))

        axios.get('http://127.0.0.1:8005/api/books/',{headers}).then(response => {
            this.setState(
                {
                    'books': response.data
                }
            )
        }).catch(error => console.log(error))
    }

    set_token(token) {
        // localStorage.setItem('token',token)
        // let item = localStorage.getItem('token')
        const cookies = new Cookies()
        cookies.set('token', token)
        this.setState({'token': token},()=>this.load_data())
    }

    get_token(username, password) {
        axios.post('http://127.0.0.1:8005/api-token-auth/',
            {'username': username, password: password})
            .then(response => {
                this.set_token(response.data['token'])
            }).catch(error => alert('Не верный логин или пароль'))
    }

    is_auth(){
        return !!this.state.token
    }

    get_headers(){
        let headers = {
            'Content-Type':'applications/json'
        }

        if(this.is_auth()){
          headers['Authorization'] = `Token ${this.state.token}`
        }

        return headers
    }

    logout() {
        this.set_token('')
    }

    get_token_from_cookies(){
        const cookies = new Cookies()
        const token = cookies.get('token')

        this.setState({'token': token},()=>this.load_data())
    }

    componentDidMount() {
     this.get_token_from_cookies()
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
                            <li>
                                 {this.is_auth()? <button onClick={()=> this.logout()}>Logout</button>:
                                     <Link to='/login'>Login</Link>}
                            </li>
                        </ul>
                    </nav>

                    <Switch>
                        <Route exact path='/' component={() => <AuthorList authors={this.state.authors}/>}/>
                        <Route exact path='/books' component={() => <BookList books={this.state.books}/>}/>

                        <Route path='/author/:id'>
                            <BookListAuthors books={this.state.books} authors={this.state.authors}/>
                        </Route>

                        <Route exact path='/login' component={() => <LoginForm
                            get_token={(username, password) => this.get_token(username, password)}/>}/>


                        <Redirect from='/book' to='/books'/>
                        <Route component={NotFound404}/>
                    </Switch>
                </BrowserRouter>
            </div>
        );
    }
}

export default App;
