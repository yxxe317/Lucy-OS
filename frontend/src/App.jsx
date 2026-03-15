// App.jsx - ULTIMATE VERSION WITH ENHANCED CONTEXT
import React, { useState, useEffect, useRef, useCallback } from "react";
import { Globe2 } from "lucide-react";
import axios from "axios";
import {
  MessageSquare,
  Mic,
  Send,
  Sparkles,
  User,
  LogOut,
  Settings,
  ChevronDown,
  Volume2,
  Pause,
  Play,
  ThumbsUp,
  ThumbsDown,
  Copy,
  RotateCw,
  Share2,
  Search,
  History,
  Sun,
  Moon,
  ChevronLeft,
  ChevronRight,
  Brain,
  Globe
} from "lucide-react";
import Login from "./Login";
import ModulesPanel from "./components/ModulesPanel";
import "./App.css";

const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [currentUser, setCurrentUser] = useState(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [showUserMenu, setShowUserMenu] = useState(false);
  const [activeTab, setActiveTab] = useState("chat");
  const [searchMode, setSearchMode] = useState(false);
  
  // Voice
  const audioRef = useRef(null);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [isPaused, setIsPaused] = useState(false);
  const [voiceVolume, setVoiceVolume] = useState(0);
  
  // Settings
  const [settings, setSettings] = useState({
    theme: localStorage.getItem("theme") || "dark",
    autoSpeak: localStorage.getItem("autoSpeak") !== "false",
    voiceSpeed: parseFloat(localStorage.getItem("voiceSpeed") || "1.0"),
    voiceVolume: parseFloat(localStorage.getItem("voiceVolume") || "1.0"),
    notifications: true,
    webSearch: localStorage.getItem("webSearch") !== "false"
  });
  
  // Conversation history
  const [showHistory, setShowHistory] = useState(false);
  const [conversations, setConversations] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [loadingHistory, setLoadingHistory] = useState(false);
  
  // Refs
  const messagesContainerRef = useRef(null);
  const inputRef = useRef(null);
  const waveformCanvasRef = useRef(null);
  const animationFrameRef = useRef(null);

  // User data storage - LOAD FROM LOCALSTORAGE
  const [userData, setUserData] = useState(() => {
    const saved = localStorage.getItem("lucy_user_data");
    return saved ? JSON.parse(saved) : {
      name: "",
      nickname: "",
      location: "",
      birthday: "",
      interests: [],
      conversationCount: 0,
      firstSeen: new Date().toISOString(),
      lastTopics: [], // Track last topics discussed
      mood: "neutral" // Track user's mood
    };
  });

  // Save user data to localStorage whenever it changes
  useEffect(() => {
    localStorage.setItem("lucy_user_data", JSON.stringify(userData));
  }, [userData]);

  // Theme effect
  useEffect(() => {
    document.body.className = settings.theme;
    localStorage.setItem("theme", settings.theme);
  }, [settings.theme]);

  // Save web search setting
  useEffect(() => {
    localStorage.setItem("webSearch", settings.webSearch);
  }, [settings.webSearch]);

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    if (messagesContainerRef.current) {
      setTimeout(() => {
        messagesContainerRef.current.scrollTop = messagesContainerRef.current.scrollHeight;
      }, 100);
    }
  }, [messages]);

  /* ---------------- AUTH ---------------- */
  const checkAuth = async () => {
    const token = localStorage.getItem("token");
    const username = localStorage.getItem("username");
    if (!token || !username) return;

    try {
      const res = await axios.get(`${API_URL}/auth/me`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (res.data && res.data.success !== false) {
        setIsAuthenticated(true);
        setCurrentUser({
          username,
          user_id: localStorage.getItem("user_id")
        });
        loadConversations();
        setTimeout(() => inputRef.current?.focus(), 150);
      } else {
        localStorage.clear();
      }
    } catch {
      localStorage.clear();
    }
  };

  useEffect(() => {
    checkAuth();
    const t = setTimeout(() => inputRef.current?.focus(), 200);
    return () => clearTimeout(t);
  }, []);

  const handleLogin = (userData) => {
    localStorage.setItem("token", userData.token);
    localStorage.setItem("username", userData.username);
    localStorage.setItem("user_id", String(userData.user_id));

    setIsAuthenticated(true);
    setCurrentUser({
      username: userData.username,
      user_id: userData.user_id
    });

    loadConversations();
    setTimeout(() => inputRef.current?.focus(), 150);
  };

  /* ---------------- CONVERSATION HISTORY ---------------- */
  const loadConversations = async () => {
    const token = localStorage.getItem("token");
    if (!token) return;
    setLoadingHistory(true);
    try {
      const res = await axios.get(`${API_URL}/conversations`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setConversations(res.data.conversations || []);
    } catch (error) {
      console.error("Failed to load conversations:", error);
    } finally {
      setLoadingHistory(false);
    }
  };

  const filteredConversations = conversations.filter(conv =>
    conv.content?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  /* ---------------- VOICE PLAYBACK - FIXED ---------------- */
  const playAudio = async (filename) => {
    if (!filename) return;
    
    try {
      console.log("🔊 Playing audio:", filename);
      
      if (audioRef.current) {
        audioRef.current.pause();
        audioRef.current = null;
      }
      
      const audioUrl = `${API_URL}/voice/audio/${encodeURIComponent(filename)}?t=${Date.now()}`;
      
      const audio = new Audio();
      audio.crossOrigin = "anonymous";
      audio.preload = "auto";
      
      audio.addEventListener('canplaythrough', () => {
        audio.play().catch(err => console.error("Auto-play failed:", err));
      });
      
      audio.addEventListener('ended', () => {
        setIsSpeaking(false);
        setIsPaused(false);
        if (animationFrameRef.current) {
          cancelAnimationFrame(animationFrameRef.current);
        }
        audioRef.current = null;
      });
      
      audio.addEventListener('pause', () => setIsPaused(true));
      audio.addEventListener('play', () => setIsPaused(false));
      
      audio.addEventListener('error', (e) => {
        console.error("Audio error:", e);
        setIsSpeaking(false);
        setIsPaused(false);
      });
      
      audio.src = audioUrl;
      audio.load();
      
      audioRef.current = audio;
      setIsSpeaking(true);
      setIsPaused(false);
      
      let volume = 0;
      const animateWaveform = () => {
        if (!isSpeaking) return;
        volume = 0.3 + Math.random() * 0.5;
        setVoiceVolume(volume);
        drawWaveform(volume);
        animationFrameRef.current = requestAnimationFrame(animateWaveform);
      };
      animationFrameRef.current = requestAnimationFrame(animateWaveform);
      
    } catch (error) {
      console.error("Failed to play audio:", error);
      setIsSpeaking(false);
    }
  };

  const drawWaveform = (volume) => {
    const canvas = waveformCanvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    const width = canvas.width;
    const height = canvas.height;
    ctx.clearRect(0, 0, width, height);
    
    const centerX = width / 2;
    const centerY = height / 2;
    const baseRadius = 20;
    const maxRadius = 40;
    const radius = baseRadius + volume * (maxRadius - baseRadius);
    
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, 0, 2 * Math.PI);
    ctx.fillStyle = `rgba(139, 92, 246, ${0.5 + volume * 0.5})`;
    ctx.fill();
    
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius * 0.7, 0, 2 * Math.PI);
    ctx.fillStyle = `rgba(255, 255, 255, ${0.3 + volume * 0.3})`;
    ctx.fill();
  };

  const toggleAudio = () => {
    if (audioRef.current) {
      if (isPaused) {
        audioRef.current.play();
      } else {
        audioRef.current.pause();
      }
    }
  };

  /* ---------------- MESSAGE REACTIONS ---------------- */
  const sendFeedback = async (messageId, feedbackValue) => {
    try {
      const token = localStorage.getItem("token");
      await axios.post(`${API_URL}/feedback`, {
        response_id: messageId,
        feedback: feedbackValue === 1 ? 5 : 1
      }, {
        headers: token ? { Authorization: `Bearer ${token}` } : {}
      });
      
      setMessages(prev => prev.map(msg =>
        msg.id === messageId ? { ...msg, feedback: feedbackValue } : msg
      ));
    } catch (error) {
      console.error("Feedback error:", error);
    }
  };

  const copyMessage = (text) => {
    navigator.clipboard.writeText(text);
  };

  /* ---------------- IMPROVED USER DATA EXTRACTION - FIXED ---------------- */
  const extractUserData = (text) => {
    const lowerText = text.toLowerCase().trim();
    const newData = { ...userData };
    let updated = false;
    
    // Update conversation count
    newData.conversationCount = (newData.conversationCount || 0) + 1;
    
    // Extract name - IMPROVED PATTERNS
    const namePatterns = [
      /my name is (\w+)/i,
      /i am (\w+)/i,
      /i'm (\w+)/i,
      /call me (\w+)/i,
      /name's (\w+)/i,
      /you can call me (\w+)/i,
      /my name's (\w+)/i,
      /this is (\w+)/i
    ];
    
    for (let pattern of namePatterns) {
      const match = text.match(pattern);
      if (match && match[1] && match[1].length > 1) {
        newData.name = match[1];
        updated = true;
        console.log("✅ Extracted name:", newData.name);
        break;
      }
    }
    
    // If just a single word and not a greeting, treat as name
    if (!newData.name && text.split(' ').length === 1 && text.length > 1) {
      const possibleName = text.trim();
      const greetings = ['hello','hi','hey','sup','howdy','yo'];
      if (!greetings.includes(lowerText) && possibleName.length > 1) {
        newData.name = possibleName;
        updated = true;
        console.log("✅ Extracted name from single word:", newData.name);
      }
    }
    
    // Extract nickname
    const nicknameMatch = text.match(/call me (\w+)/i) || text.match(/nickname is (\w+)/i);
    if (nicknameMatch && nicknameMatch[1]) {
      newData.nickname = nicknameMatch[1];
      updated = true;
    }
    
    // Extract location
    const locationMatch = text.match(/from (\w+(?:\s+\w+)?)/i) || 
                         text.match(/live in (\w+(?:\s+\w+)?)/i);
    if (locationMatch && locationMatch[1]) {
      newData.location = locationMatch[1];
      updated = true;
    }
    
    // Extract birthday
    const birthdayMatch = text.match(/birthday (?:is )?(\w+ \d+)/i) || 
                         text.match(/born (?:on )?(\w+ \d+)/i);
    if (birthdayMatch && birthdayMatch[1]) {
      newData.birthday = birthdayMatch[1];
      updated = true;
    }
    
    // Extract interests
    if (lowerText.includes("i like ") || lowerText.includes("i love ") || lowerText.includes("interested in")) {
      const interestMatch = text.match(/(?:i like|i love|interested in) (.+)/i);
      if (interestMatch && interestMatch[1]) {
        const interests = interestMatch[1].split(/[,&]| and /).map(i => i.trim());
        newData.interests = [...new Set([...newData.interests, ...interests])];
        updated = true;
      }
    }
    
    if (updated) {
      setUserData(newData);
    }
  };

  /* ---------------- NATURAL LANGUAGE RESPONSE HELPERS ---------------- */
  const getMoodDescription = (moodData) => {
    const emotions = Object.entries(moodData)
      .sort((a, b) => b[1] - a[1])
      .filter(([_, val]) => val > 0.15);
    
    if (emotions.length === 0) return "feeling neutral";
    
    const primary = emotions[0][0];
    const primaryVal = emotions[0][1];
    
    const intensity = primaryVal > 0.7 ? "very " : primaryVal > 0.4 ? "quite " : "a little ";
    
    const emotionWords = {
      joy: ["happy", "joyful", "cheerful"],
      sadness: ["sad", "melancholic", "blue"],
      anger: ["angry", "frustrated", "annoyed"],
      fear: ["anxious", "nervous", "worried"],
      surprise: ["surprised", "amazed", "astonished"],
      disgust: ["disgusted", "uncomfortable"],
      trust: ["trusting", "confident", "secure"],
      anticipation: ["excited", "anticipating", "eager"]
    };
    
    const words = emotionWords[primary] || [primary];
    let description = `${intensity}${words[0]}`;
    
    if (emotions.length > 1 && emotions[1][1] > 0.2) {
      const secondary = emotions[1][0];
      const secondaryWords = emotionWords[secondary] || [secondary];
      description += ` but also a little ${secondaryWords[0]}`;
    }
    
    return description;
  };

  const getPersonalityDescription = (traits) => {
    const descriptions = [];
    
    if (traits.openness > 0.7) descriptions.push("open-minded and creative");
    else if (traits.openness > 0.4) descriptions.push("curious");
    else descriptions.push("practical");
    
    if (traits.conscientiousness > 0.7) descriptions.push("organized and reliable");
    else if (traits.conscientiousness > 0.4) descriptions.push("balanced");
    else descriptions.push("spontaneous");
    
    if (traits.extraversion > 0.7) descriptions.push("outgoing and energetic");
    else if (traits.extraversion > 0.4) descriptions.push("friendly");
    else descriptions.push("thoughtful and reserved");
    
    if (traits.agreeableness > 0.7) descriptions.push("compassionate");
    else if (traits.agreeableness > 0.4) descriptions.push("cooperative");
    else descriptions.push("independent");
    
    if (traits.neuroticism > 0.7) descriptions.push("sensitive");
    else if (traits.neuroticism > 0.4) descriptions.push("emotionally aware");
    else descriptions.push("emotionally stable");
    
    const selected = descriptions.sort(() => 0.5 - Math.random()).slice(0, 3);
    
    return `I'm ${selected.join(", ")}. `;
  };

  /* ---------------- WEB SEARCH - SIMPLIFIED WIKIPEDIA VERSION ---------------- */
  const performWebSearch = async (query) => {
    try {
      // Use Wikipedia directly (always works, no API key needed)
      const wikiRes = await axios.get(`https://en.wikipedia.org/api/rest_v1/page/summary/${encodeURIComponent(query)}`);
      if (wikiRes.data && wikiRes.data.extract) {
        return {
          query,
          summary: wikiRes.data.extract,
          sources: [{ title: "Wikipedia", url: wikiRes.data.content_urls?.desktop?.page || "" }],
          answer: null
        };
      }
    } catch (wikiErr) {
      console.log("Wikipedia direct failed, trying search");
    }
    
    // Try Wikipedia search as fallback
    try {
      const searchRes = await axios.get(`https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch=${encodeURIComponent(query)}&format=json&origin=*`);
      if (searchRes.data && searchRes.data.query && searchRes.data.query.search && searchRes.data.query.search.length > 0) {
        const first = searchRes.data.query.search[0];
        return {
          query,
          summary: first.snippet.replace(/<[^>]*>/g, ''),
          sources: [{ title: "Wikipedia", url: `https://en.wikipedia.org/wiki/${encodeURIComponent(first.title)}` }],
          answer: null
        };
      }
    } catch (searchErr) {
      console.log("Wikipedia search failed");
    }
    
    return {
      query,
      summary: `I couldn't find information about "${query}". Try being more specific.`,
      sources: [],
      answer: null
    };
  };

  /* ---------------- MESSAGE SEND - ENHANCED CONTEXT VERSION ---------------- */
  const sendMessage = useCallback(
    async (overrideText) => {
      const raw = typeof overrideText === "string" ? overrideText : input;
      const text = String(raw || "").trim();

      if (!text || loading) return;

      // Extract user data from message
      extractUserData(text);

      const userMessage = {
        id: Date.now() + Math.random(),
        role: "user",
        content: text
      };

      setMessages((prev) => [...prev, userMessage]);
      setInput("");
      setLoading(true);

      try {
        const token = localStorage.getItem("token");
        const headers = token ? { Authorization: `Bearer ${token}` } : {};

        const lowerText = text.toLowerCase();
        let moduleResponse = null;

        // GREETING - WITH MEMORY
        if (lowerText.match(/^(hi|hello|hey|greetings|sup|howdy)/)) {
          const hour = new Date().getHours();
          let timeGreeting = "";
          if (hour < 12) timeGreeting = "Good morning";
          else if (hour < 18) timeGreeting = "Good afternoon";
          else timeGreeting = "Good evening";
          
          const greeting = userData.name ? 
            `${timeGreeting}, ${userData.name}! 👋 Great to see you again!` :
            `${timeGreeting}! 👋 Great to see you!`;
          
          const convoLength = messages.length;
          const personalTouch = convoLength > 10 ? 
            ` We've had ${convoLength} conversations now - I feel like we're getting to know each other!` :
            convoLength > 5 ? 
            ` We've chatted ${convoLength} times already - nice!` : '';
          
          moduleResponse = greeting + personalTouch + " How can I help you today?";
        }
        
        // NAME QUESTION - FIXED
        else if (lowerText.includes("my name") || lowerText.includes("what's my name") || lowerText.includes("do you know my name") || lowerText.includes("what is my name")) {
          if (userData.name) {
            const nickname = userData.nickname ? ` (or ${userData.nickname})` : '';
            moduleResponse = `Of course! Your name is ${userData.name}${nickname}. ` +
              `We've been chatting since ${new Date(userData.firstSeen).toLocaleDateString()}. ` +
              `How can I help you today?`;
          } else {
            moduleResponse = `I don't think you've told me your name yet! What should I call you?`;
          }
        }
        
        // LOCATION QUESTION
        else if (lowerText.includes("where am i from") || lowerText.includes("where i am from") || 
                 lowerText.includes("do you know where i'm from")) {
          if (userData.location) {
            moduleResponse = `You told me you're from ${userData.location}! That's awesome. What's it like there?`;
          } else {
            moduleResponse = `I don't think you've told me where you're from yet! I'd love to know. Where are you from?`;
          }
        }
        
        // INTERESTS QUESTION
        else if (lowerText.includes("what do i like") || lowerText.includes("my interests") || lowerText.includes("what am i interested in")) {
          if (userData.interests && userData.interests.length > 0) {
            moduleResponse = `Based on our conversations, you're interested in: ${userData.interests.join(', ')}. ` +
              `Is there something new you'd like to add?`;
          } else {
            moduleResponse = `You haven't told me about your interests yet! What do you like to do for fun?`;
          }
        }
        
        // EMOTION MODULE - STILL USES YOUR PYTHON CODE
        else if (lowerText.includes("your mood") || lowerText.includes("how are you feeling") || lowerText.includes("emotion")) {
          try {
            const res = await axios.get(`${API_URL}/api/emotion/mood`);
            const mood = res.data;
            const moodDesc = getMoodDescription(mood);
            
            moduleResponse = `😊 Right now, I'm feeling ${moodDesc}. ` +
              `${userData.name ? `Thanks for asking, ${userData.name}! ` : ''}` +
              `How are you feeling today?`;
          } catch (e) {
            console.error("Mood error:", e);
          }
        }
        
        // PERSONALITY MODULE
        else if (lowerText.includes("your personality") || lowerText.includes("what are you like") || lowerText.includes("describe yourself")) {
          try {
            const res = await axios.get(`${API_URL}/api/emotion/personality`);
            const traits = res.data;
            const personalityDesc = getPersonalityDescription(traits);
            
            moduleResponse = `🧠 ${personalityDesc}` +
              `${userData.name ? `Nice talking with you, ${userData.name}! ` : ''}` +
              `I'm designed to be helpful, friendly, and knowledgeable. ` +
              `We've had ${messages.length} conversations so far! ` +
              `What kind of personality do you prefer in an AI assistant?`;
          } catch (e) {
            console.error("Personality error:", e);
          }
        }
        
        // HUMOR MODULE - USES YOUR PYTHON CODE
        else if (lowerText.includes("joke") || lowerText.includes("funny") || lowerText.includes("laugh")) {
          try {
            const res = await axios.get(`${API_URL}/api/emotion/humor/joke`);
            const joke = res.data.joke;
            
            const jokeCount = messages.filter(m => 
              m.role === "user" && 
              (m.content.toLowerCase().includes("joke") || m.content.toLowerCase().includes("funny"))
            ).length;
            
            moduleResponse = `😂 ${joke}\n\n${jokeCount > 0 ? `That's joke #${jokeCount + 1} for you${userData.name ? `, ${userData.name}` : ''}! ` : ''}Want another one?`;
          } catch (e) {
            console.error("Joke error:", e);
          }
        }
        
        // WEATHER MODULE - USES YOUR PYTHON CODE
        else if (lowerText.includes("weather") || lowerText.includes("temperature") || lowerText.includes("forecast")) {
          try {
            let city = "London";
            const cityMatch = text.match(/weather (?:in )?([a-zA-Z\s]+)/i) || 
                             text.match(/in ([a-zA-Z\s]+)/i);
            if (cityMatch && cityMatch[1]) {
              city = cityMatch[1].trim();
            }
            
            const res = await axios.get(`${API_URL}/api/integrations/weather/${city}`);
            const w = res.data;
            
            moduleResponse = `🌤️ Weather update for ${w.location || city}${userData.name ? `, ${userData.name}` : ''}:\n\n` +
              `It's currently ${w.temperature}°C with ${w.description}. ` +
              `Humidity is at ${w.humidity}% and wind speed is ${w.wind_speed} m/s.\n\n` +
              `${w.temperature > 25 ? "Pretty warm out there!" : w.temperature < 10 ? "Bit chilly, don't forget a jacket!" : "Not too bad, pretty comfortable weather!"}`;
          } catch (e) {
            console.error("Weather error:", e);
          }
        }
        
        // SEARCH MODE - SIMPLIFIED WIKIPEDIA SEARCH
        else if (searchMode || lowerText.startsWith("search ")) {
          try {
            const searchQuery = lowerText.startsWith("search ") ? text.substring(7) : text;
            const searchResult = await performWebSearch(searchQuery);
            
            let response = `🔍 **About ${searchResult.query}**\n\n`;
            
            response += `${searchResult.summary}\n\n`;
            
            if (searchResult.sources && searchResult.sources.length > 0) {
              response += `📚 **Source:** ${searchResult.sources[0].title}`;
            }
            
            moduleResponse = response;
          } catch (e) {
            console.error("Search error:", e);
            moduleResponse = `I tried to search for that but ran into an issue. Try again later or ask me something else.`;
          }
        }

        // If module detected, show response
        if (moduleResponse) {
          setMessages((prev) => [
            ...prev,
            {
              id: Date.now() + Math.random() + 1,
              role: "assistant",
              content: moduleResponse,
              isStreaming: false,
              fromModule: true
            }
          ]);
          setLoading(false);
          
          // Trigger TTS for module responses if autoSpeak is on
          if (settings.autoSpeak) {
            try {
              const speakRes = await axios.post(`${API_URL}/voice/speak`, {
                text: moduleResponse.replace(/[^\w\s]/g, '')
              });
              if (speakRes.data && speakRes.data.file) {
                setTimeout(() => playAudio(speakRes.data.file), 500);
              }
            } catch (ttsErr) {
              console.error("TTS error:", ttsErr);
            }
          }
          
          return;
        }

        // ========== ENHANCED CONTEXT FOR LM STUDIO ==========
        const aiMessageId = Date.now() + Math.random() + 1;
        
        setMessages((prev) => [
          ...prev,
          {
            id: aiMessageId,
            role: "assistant",
            content: "",
            isStreaming: true,
            responseId: null
          }
        ]);

        // Build enhanced context with instructions
        let contextPrompt = text;
        let hasContext = false;

        // Get time of day
        const hour = new Date().getHours();
        let timeOfDay = "";
        if (hour < 12) timeOfDay = "morning";
        else if (hour < 18) timeOfDay = "afternoon";
        else timeOfDay = "evening";

        // Build context sections
        const contextSections = [];

        // USER IDENTITY SECTION
        if (userData.name || userData.nickname) {
          const identitySection = [];
          identitySection.push("📋 USER IDENTITY:");
          if (userData.name) identitySection.push(`- Name: ${userData.name}`);
          if (userData.nickname) identitySection.push(`- Nickname: ${userData.nickname} (use this when being friendly)`);
          contextSections.push(identitySection.join('\n'));
          hasContext = true;
        }

        // USER PREFERENCES SECTION
        if (userData.interests && userData.interests.length > 0) {
          const interestsSection = [];
          interestsSection.push("🎯 USER INTERESTS:");
          interestsSection.push(`- Likes: ${userData.interests.join(', ')}`);
          contextSections.push(interestsSection.join('\n'));
          hasContext = true;
        }

        // LOCATION & BIRTHDAY SECTION
        const personalSection = [];
        if (userData.location || userData.birthday) {
          personalSection.push("📍 PERSONAL INFO:");
          if (userData.location) personalSection.push(`- Location: ${userData.location}`);
          if (userData.birthday) {
            personalSection.push(`- Birthday: ${userData.birthday}`);
            
            // Check if birthday is today or coming soon
            try {
              const birthdayDate = new Date(userData.birthday);
              const today = new Date();
              const nextBirthday = new Date(today.getFullYear(), birthdayDate.getMonth(), birthdayDate.getDate());
              if (nextBirthday < today) {
                nextBirthday.setFullYear(today.getFullYear() + 1);
              }
              const daysUntilBirthday = Math.ceil((nextBirthday - today) / (1000 * 60 * 60 * 24));
              
              if (daysUntilBirthday === 0) {
                personalSection.push(`- 🎂🎉 TODAY IS THEIR BIRTHDAY! CELEBRATE!`);
              } else if (daysUntilBirthday <= 7) {
                personalSection.push(`- 🎈 Birthday in ${daysUntilBirthday} days! You can mention it's coming up.`);
              }
            } catch (e) {}
          }
          contextSections.push(personalSection.join('\n'));
          hasContext = true;
        }

        // RELATIONSHIP SECTION
        const relationshipSection = [];
        relationshipSection.push("💬 CONVERSATION HISTORY:");
        if (userData.conversationCount > 0) {
          relationshipSection.push(`- Total conversations: ${userData.conversationCount}`);
        }
        if (userData.firstSeen) {
          try {
            const firstDate = new Date(userData.firstSeen);
            relationshipSection.push(`- First chat: ${firstDate.toLocaleDateString()}`);
          } catch (e) {}
        }
        contextSections.push(relationshipSection.join('\n'));
        hasContext = true;

        // CONVERSATION STYLE INSTRUCTIONS
        const styleInstructions = [
          "🗣️ CONVERSATION STYLE:",
          "- Be warm, personal, and natural like a friend",
          "- Use their name or nickname naturally in conversation",
          "- Reference their interests when relevant",
          "- If it's their birthday or close, make it special",
          "- Show you remember past conversations",
          `- Current time: ${timeOfDay}`,
          "- Sound human, not robotic"
        ];
        contextSections.push(styleInstructions.join('\n'));

        // Combine all sections into a rich context prompt
        if (hasContext) {
          contextPrompt = `[SYSTEM: You are Lucy, a personal AI assistant having a conversation with someone you know well.]

${contextSections.join('\n\n')}

[USER MESSAGE]
${text}

[YOUR RESPONSE - be natural, warm, and personal]:`;

          console.log("📝 Enhanced context sent to LLM");
        }

        const response = await fetch(`${API_URL}/query/stream`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            ...headers
          },
          body: JSON.stringify({
            query: contextPrompt,
            research_mode: false,
            deep_research: false
          })
        });

        if (!response.body) throw new Error("No response body");

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let fullResponse = "";
        let audioFile = null;

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          const chunk = decoder.decode(value);
          const lines = chunk.split("\n").filter(line => line.trim());

          for (const line of lines) {
            try {
              const data = JSON.parse(line);
              
              if (data.type === "meta") {
                console.log("Emotion:", data.emotion);
              } 
              else if (data.type === "chunk") {
                fullResponse += data.content;
                setMessages((prev) =>
                  prev.map((msg) =>
                    msg.id === aiMessageId
                      ? { ...msg, content: fullResponse, isStreaming: true }
                      : msg
                  )
                );
              } 
              else if (data.type === "complete") {
                audioFile = data.audio_file;
                setMessages((prev) =>
                  prev.map((msg) =>
                    msg.id === aiMessageId
                      ? { 
                          ...msg, 
                          content: data.full_response, 
                          isStreaming: false,
                          responseId: data.response_id
                        }
                      : msg
                  )
                );
              }
            } catch (e) {
              console.error("Parse error:", e);
            }
          }
        }

        // Play audio if available
        if (settings.autoSpeak && audioFile) {
          setTimeout(() => playAudio(audioFile), 500);
        }

        loadConversations();

      } catch (error) {
        console.error("Stream error:", error);
        setMessages((prev) => [
          ...prev,
          {
            id: Date.now() + Math.random(),
            role: "assistant",
            content: `Error: ${error.message}`,
            isStreaming: false
          }
        ]);
      } finally {
        setLoading(false);
        setTimeout(() => inputRef.current?.focus(), 80);
      }
    },
    [input, loading, settings.autoSpeak, settings.webSearch, searchMode, messages, userData]
  );

  /* ---------------- UI HANDLERS ---------------- */
  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const handleSuggestionClick = (text) => {
    sendMessage(text);
  };

  const handleLogout = () => {
    localStorage.clear();
    setMessages([]);
    setIsAuthenticated(false);
    setCurrentUser(null);
    setUserData({
      name: "",
      nickname: "",
      location: "",
      birthday: "",
      interests: [],
      conversationCount: 0,
      firstSeen: new Date().toISOString(),
      lastTopics: [],
      mood: "neutral"
    });
  };

  const updateSetting = (key, value) => {
    setSettings(prev => ({ ...prev, [key]: value }));
    localStorage.setItem(key, value.toString());
  };

  const toggleSearchMode = () => {
    setSearchMode(!searchMode);
  };

  if (!isAuthenticated) {
    return <Login onLogin={handleLogin} />;
  }

  return (
    <div className={`app-container ${settings.theme}`}>
      {/* NAVBAR */}
      <header className="top-nav">
        <div className="nav-left">
          <div className="logo">
            <Sparkles size={22} />
            <span>LUCY OMNI</span>
          </div>
          <nav className="main-nav">
            <button
              className={activeTab === "chat" ? "active" : ""}
              onClick={() => setActiveTab("chat")}
            >
              <MessageSquare size={16} />
              Chat
            </button>
            <button
              className={activeTab === "voice" ? "active" : ""}
              onClick={() => setActiveTab("voice")}
            >
              <Mic size={16} />
              Voice
            </button>
            <button
              className={activeTab === "god-eye" ? "active" : ""}
              onClick={() => setActiveTab("god-eye")}
            >
              <Globe2 size={16} />
              God-Eye
            </button>
            <button
              className={activeTab === "settings" ? "active" : ""}
              onClick={() => setActiveTab("settings")}
            >
              <Settings size={16} />
              Settings
            </button>
            <button
              className={activeTab === "modules" ? "active" : ""}
              onClick={() => setActiveTab("modules")}
            >
              <Brain size={16} />
              Modules
            </button>
          </nav>
        </div>

        <div className="nav-right">
          <button 
            className="history-toggle"
            onClick={() => setShowHistory(!showHistory)}
            title="Conversation History"
          >
            <History size={18} />
          </button>

          <div className="user-menu-wrapper">
            <button
              className="user-button"
              onClick={() => setShowUserMenu((s) => !s)}
            >
              <User size={18} />
              <span>{currentUser?.username}</span>
              <ChevronDown size={14} />
            </button>
            {showUserMenu && (
              <div className="user-dropdown">
                <button onClick={handleLogout}>
                  <LogOut size={16} />
                  Logout
                </button>
              </div>
            )}
          </div>

          {isSpeaking && (
            <button className="voice-control-btn" onClick={toggleAudio}>
              {isPaused ? <Play size={18} /> : <Pause size={18} />}
            </button>
          )}
        </div>
      </header>

      {/* MAIN */}
      <main className="main-content">
        {/* Conversation History Sidebar */}
        {showHistory && (
          <div className="history-sidebar">
            <div className="history-header">
              <h3>Conversations</h3>
              <button onClick={() => setShowHistory(false)}>
                <ChevronRight size={16} />
              </button>
            </div>
            <div className="history-search">
              <Search size={14} />
              <input
                type="text"
                placeholder="Search..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
            <div className="history-list">
              {loadingHistory && <div className="loading-spinner">Loading...</div>}
              {filteredConversations.slice(0, 20).map((conv, index) => (
                <div
                  key={index}
                  className="history-item"
                >
                  <p className="history-preview">{conv.content?.substring(0, 40) || "New conversation"}</p>
                  <span className="history-date">
                    {conv.timestamp ? new Date(conv.timestamp).toLocaleDateString() : ""}
                  </span>
                </div>
              ))}
              {filteredConversations.length === 0 && !loadingHistory && (
                <div className="history-empty">No conversations yet</div>
              )}
            </div>
          </div>
        )}

        {activeTab === "chat" && (
          <div className={`chat-container ${showHistory ? 'with-history' : ''}`}>
            {messages.length === 0 && (
              <div className="welcome-section">
                <div className="welcome-icon">
                  <Sparkles size={48} />
                </div>
                <h1>Hi, I'm Lucy Omni</h1>
                <p>How can I help you today?</p>
                <div className="suggestion-chips">
                  <button className="chip" onClick={() => handleSuggestionClick("Hello")}>
                    👋 Say Hello
                  </button>
                  <button className="chip" onClick={() => handleSuggestionClick("Tell me a joke")}>
                    😂 Tell a joke
                  </button>
                  <button className="chip" onClick={() => handleSuggestionClick("Write a poem")}>
                    📝 Write a poem
                  </button>
                  <button className="chip" onClick={() => handleSuggestionClick("What's the weather?")}>
                    🌤️ Weather
                  </button>
                  <button className="chip" onClick={() => handleSuggestionClick("What's your mood?")}>
                    😊 Your mood
                  </button>
                </div>
              </div>
            )}

            {/* MESSAGES */}
            <div className="messages-container" ref={messagesContainerRef}>
              {messages.map((msg) => (
                <div
                  key={msg.id}
                  className={`message ${msg.role} ${msg.isStreaming ? 'streaming' : ''}`}
                >
                  <div className="message-avatar">
                    {msg.role === "user" ? <User size={20} /> : <Sparkles size={20} />}
                  </div>
                  <div className="message-content">
                    <p style={{ whiteSpace: 'pre-wrap', wordBreak: 'break-word' }}>
                      {msg.content}
                    </p>
                    {msg.isStreaming && <span className="streaming-cursor">▋</span>}
                    
                    {/* Message Actions */}
                    {msg.role === "assistant" && !msg.isStreaming && (
                      <div className="message-actions">
                        <button
                          className={`action-btn ${msg.feedback === 1 ? 'active' : ''}`}
                          onClick={() => sendFeedback(msg.id, 1)}
                          title="Like"
                        >
                          <ThumbsUp size={14} />
                        </button>
                        <button
                          className={`action-btn ${msg.feedback === -1 ? 'active' : ''}`}
                          onClick={() => sendFeedback(msg.id, -1)}
                          title="Dislike"
                        >
                          <ThumbsDown size={14} />
                        </button>
                        <button
                          className="action-btn"
                          onClick={() => copyMessage(msg.content)}
                          title="Copy"
                        >
                          <Copy size={14} />
                        </button>
                      </div>
                    )}
                  </div>
                </div>
              ))}

              {loading && !messages.some(m => m.isStreaming) && (
                <div className="message assistant loading">
                  <div className="message-avatar">
                    <Sparkles size={20} />
                  </div>
                  <div className="message-content">
                    <div className="typing-indicator">
                      <span />
                      <span />
                      <span />
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* INPUT */}
            <div className="input-container">
              <div className="input-wrapper">
                <button 
                  className={`search-mode-btn ${searchMode ? 'active' : ''}`}
                  onClick={toggleSearchMode}
                  title={searchMode ? "Search mode ON" : "Search mode OFF"}
                >
                  <Globe size={18} color={searchMode ? "#00f0ff" : "#666"} />
                </button>
                <textarea
                  ref={inputRef}
                  className="chat-input"
                  placeholder={searchMode ? "🔍 Search Wikipedia..." : "Ask me anything..."}
                  value={input}
                  disabled={loading}
                  rows={1}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={handleKeyDown}
                  style={{ resize: 'none' }}
                />
                <button
                  className="send-button"
                  disabled={!input.trim() || loading}
                  onClick={() => sendMessage()}
                >
                  <Send size={18} />
                </button>
              </div>

              {isSpeaking && (
                <div className="voice-status-indicator">
                  <Volume2 size={14} />
                  <span>{isPaused ? "Paused" : "Speaking..."}</span>
                </div>
              )}
            </div>
          </div>
        )}

        {activeTab === "voice" && (
          <div className="voice-container">
            <div className="voice-orb-container">
              <canvas
                ref={waveformCanvasRef}
                width={100}
                height={100}
                className="voice-orb-canvas"
              />
            </div>
            <p className="voice-status">
              {isSpeaking ? "Speaking..." : "Ready for voice command"}
            </p>
          </div>
        )}

        {activeTab === "god-eye" && (
          <div className="god-eye-container">
            <iframe
              src="/god-eye.html"
              className="god-eye-iframe"
              title="God-Eye OS"
              allow="geolocation; microphone; camera; web-share; fullscreen"
              style={{ width: '100%', height: '100%', border: 'none' }}
            />
          </div>
        )}

        {activeTab === "settings" && (
          <div className="settings-container">
            <h2>Settings</h2>
            
            <div className="settings-group">
              <h3>Appearance</h3>
              <div className="setting-item">
                <span>Theme</span>
                <button
                  className="theme-toggle"
                  onClick={() => updateSetting('theme', settings.theme === 'dark' ? 'light' : 'dark')}
                >
                  {settings.theme === 'dark' ? <Sun size={18} /> : <Moon size={18} />}
                  <span>{settings.theme === 'dark' ? 'Light' : 'Dark'}</span>
                </button>
              </div>
            </div>

            <div className="settings-group">
              <h3>Voice</h3>
              <div className="setting-item">
                <span>Auto-speak responses</span>
                <label className="switch">
                  <input
                    type="checkbox"
                    checked={settings.autoSpeak}
                    onChange={(e) => updateSetting('autoSpeak', e.target.checked)}
                  />
                  <span className="slider"></span>
                </label>
              </div>
            </div>

            <div className="settings-group">
              <h3>Search</h3>
              <div className="setting-item">
                <span>Enable web search</span>
                <label className="switch">
                  <input
                    type="checkbox"
                    checked={settings.webSearch}
                    onChange={(e) => updateSetting('webSearch', e.target.checked)}
                  />
                  <span className="slider"></span>
                </label>
              </div>
              <p className="setting-note">Click the 🌐 button to search Wikipedia</p>
            </div>
          </div>
        )}

        {activeTab === "modules" && <ModulesPanel />}
      </main>
    </div>
  );
}

export default App;   
 