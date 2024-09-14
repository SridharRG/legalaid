import { useState } from 'react'
import { Button } from "./Button"
import { Input } from "./Input"
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "./Card"
import { ScrollArea } from "./ScrollArea"
import { SendIcon, ShieldIcon } from 'lucide-react'

export default function LegalAideChatbot() {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: "Hello! I'm your legal aide chatbot. How can I assist you today?" }
  ])
  const [input, setInput] = useState('')

  const handleSend = () => {
    if (input.trim()) {
      setMessages([...messages, { role: 'user', content: input }])
      // Here you would typically send the input to your backend for processing
      // For this example, we'll just echo the input with a prefix
      setTimeout(() => {
        setMessages(msgs => [...msgs, { role: 'assistant', content: `Regarding your query "${input}", I would need more information to provide accurate legal advice. Could you please provide more details?` }])
      }, 1000)
      setInput('')
    }
  }

  return (
    <Card className="w-full max-w-2xl mx-auto bg-gray-900 text-white">
      <CardHeader>
        <CardTitle className="text-2xl font-bold text-center">Ask Legal Aide AI Anything</CardTitle>
        <p className="text-center text-gray-400">
          <ShieldIcon className="inline-block mr-2" />
          Seeders
        </p>
      </CardHeader>
      <CardContent>
        <ScrollArea className="h-[400px] pr-4">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`mb-4 ${
                message.role === 'user' ? 'text-right' : 'text-left'
              }`}
            >
              <div
                className={`inline-block p-2 rounded-lg ${
                  message.role === 'user' ? 'bg-blue-600' : 'bg-gray-700'
                }`}
              >
                {message.content}
              </div>
            </div>
          ))}
        </ScrollArea>
      </CardContent>
      <CardFooter>
        <form
          onSubmit={(e) => {
            e.preventDefault()
            handleSend()
          }}
          className="flex w-full items-center space-x-2"
        >
          <Input
            type="text"
            placeholder="Type your legal question..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            className="flex-grow bg-gray-800 text-white border-gray-700"
          />
          <Button type="submit" size="icon" className="bg-blue-600 hover:bg-blue-700">
            <SendIcon className="h-4 w-4" />
            <span className="sr-only">Send</span>
          </Button>
        </form>
      </CardFooter>
    </Card>
  )
}