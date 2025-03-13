// import React, { useState, useRef, useEffect } from 'react';
// import './ChatInterface.css';

// const ChatInterface = ({ onQuerySubmit }) => {
//   const [message, setMessage] = useState('');
//   const [chatHistory, setChatHistory] = useState([]);
//   const chatContainerRef = useRef(null);

//   // Scroll to bottom when chat history changes
//   useEffect(() => {
//     if (chatContainerRef.current) {
//       chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
//     }
//   }, [chatHistory]);

//   const handleSubmit = (e) => {
//     e.preventDefault();
//     if (!message.trim()) return;

//     // Add user message to chat history
//     const userMessage = {
//       type: 'user',
//       text: message,
//       timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
//     };
//     setChatHistory([...chatHistory, userMessage]);

//     // Submit query to parent component
//     onQuerySubmit(message);

//     // Clear input
//     setMessage('');
//   };

//   // Add bot response to chat history
//   const addBotResponse = (text) => {
//     const botMessage = {
//       type: 'bot',
//       text,
//       timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
//     };
//     setChatHistory([...chatHistory, botMessage]);
//   };

//   return (
//     <div className="chat-interface">
//       <div className="chat-header">
//         <h2>Shopping Assistant</h2>
//       </div>

//       <div className="chat-container" ref={chatContainerRef}>
//         {chatHistory.length === 0 ? (
//           <div className="welcome-message">
//             <h3>Welcome to our Shopping Assistant!</h3>
//             <p>Ask me anything about our products. For example:</p>
//             <ul>
//               <li>"Show me white shirts under 600 rupees"</li>
//               <li>"I need comfortable women's clothing"</li>
//               <li>"Do you have any sofa beds for my living room?"</li>
//             </ul>
//           </div>
//         ) : (
//           chatHistory.map((msg, index) => (
//             <div key={index} className={`chat-message ${msg.type}`}>
//               <div className="message-content">
//                 <p>{msg.text}</p>
//                 <span className="timestamp">{msg.timestamp}</span>
//               </div>
//             </div>
//           ))
//         )}
//       </div>

//       <form className="chat-input" onSubmit={handleSubmit}>
//         <input
//           type="text"
//           value={message}
//           onChange={(e) => setMessage(e.target.value)}
//           placeholder="Type your question here..."
//         />
//         <button type="submit">
//           <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24">
//             <path fill="none" d="M0 0h24v24H0z"/>
//             <path d="M1.946 9.315c-.522-.174-.527-.455.01-.634l19.087-6.362c.529-.176.832.12.684.638l-5.454 19.086c-.15.529-.455.547-.679.045L12 14l6-8-8 6-8.054-2.685z" fill="currentColor"/>
//           </svg>
//         </button>
//       </form>
//     </div>
//   );
// };

// export default ChatInterface;
