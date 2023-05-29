import React, { useEffect, useState } from 'react';

const Home = () => {
    const [username, setUsername] = useState('');
    const [posts, setPosts] = useState([]);
    const [users, setUsers] = useState([]);

    useEffect(() => {
        fetchData();
    }, []);

    const fetchData = async () => {
        try {
            const response = await fetch('http://127.0.0.1:5000/home/');
            const { username, post, usr } = response.data;

            setUsername(username);
            setPosts(post);
            setUsers(usr);
        } catch (error) {
            console.log(error);
        }
    };

    return (
        <div>
            <h1>Welcome to Twitter</h1>
            <h2>Logged in as: {username}</h2>

            <div>
                <h3>Posts:</h3>
                {posts.map((post) => (
                    <div key={post.id}>
                        <p>Username: {post.username}</p>
                        <p>Body: {post.body}</p>
                        <p>Created at: {post['created-at']}</p>
                        <p>Likes: {post.likes}</p>
                    </div>
                ))}
            </div>

            <div>
                <h3>Users:</h3>
                {users.map((user) => (
                    <div key={user.id}>
                        <p>Username: {user.username}</p>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Home;
