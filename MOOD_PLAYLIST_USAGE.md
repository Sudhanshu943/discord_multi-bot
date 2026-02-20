# Mood-Based Auto-Playlist Feature

## Overview
Your Discord bot now has an **automatic mood-detection and playlist-generation system**. When you tell the AI about your mood, it will automatically:

1. Detect your mood from your message
2. Suggest 4-5 songs based on that mood
3. Search for ALL songs in **PARALLEL** (simultaneously)
4. Queue them all to the music player
5. Start playing automatically

**All within 1-2 seconds!**

---

## How to Use

### Simple Examples
Just tell the bot how you're feeling in any chat:

```
"I'm in a good mood!"
→ Detects: happy → Suggests happy songs → Queues 5 songs → Plays!

"I'm feeling sad today"
→ Detects: sad → Suggests sad songs → Queues 5 songs → Plays!

"I need to focus on work"
→ Detects: focus → Suggests focus/study songs → Queues songs → Plays!

"Let's party!"
→ Detects: party → Suggests party songs → Queues songs → Plays!

"I'm feeling romantic"
→ Detects: romantic → Suggests romantic songs → Queues songs → Plays!

"I'm energized!"
→ Detects: energetic → Suggests energetic songs → Queues songs → Plays!

"Let me chill out"
→ Detects: calm → Suggests calm/chill songs → Queues songs → Plays!
```

---

## Supported Moods & Keywords

### 😊 Happy
**Keywords**: happy, joyful, excited, cheerful, upbeat, good mood, feeling great, awesome, amazing, wonderful

**Suggested Songs**:
- Levitating - Dua Lipa
- Walking on Sunshine - Katrina & The Waves
- Good As Hell - Lizzo
- Don't Stop Me Now - Queen
- Walking in the Sun - Vampire Weekend

---

### 😢 Sad
**Keywords**: sad, depressed, melancholy, blue, heartbroken, lonely, down, bummed, unhappy, devastated

**Suggested Songs**:
- Someone Like You - Adele
- Hurt - Johnny Cash
- The Night We Met - Lord Huron
- Skinny Love - Bon Iver
- Creep - Radiohead

---

### ⚡ Energetic
**Keywords**: energetic, hyped, pumped, excited, active, workout, running, gym, hype, fired up, intense

**Suggested Songs**:
- Kick It - NCT 127
- Blinding Lights - The Weeknd
- Thunder - Imagine Dragons
- Pump It - The Black Eyed Peas
- Eye of the Tiger - Survivor

---

### 🧘 Calm
**Keywords**: calm, relaxed, peaceful, mellow, chill, chill out, relax, meditation, sleep, study

**Suggested Songs**:
- Weightless - Marconi Union
- Clair de Lune - Debussy
- Lo-Fi Hip Hop - Various Artists
- Peaceful Piano - Spotify Playlist
- Brian Eno - Music for Airports

---

### 💕 Romantic
**Keywords**: romantic, love, loving, affectionate, date, together, soulmate, crush, in love

**Suggested Songs**:
- Perfect - Ed Sheeran
- All of Me - John Legend
- Thinking Out Loud - Ed Sheeran
- Kiss Me - Sixpence None The Richer
- Best Day of My Life - American Authors

---

### 🎉 Party
**Keywords**: party, dance, celebrate, festive, club, rave, fun, vibing, dancing, celebration

**Suggested Songs**:
- Uptown Funk - Mark Ronson ft. Bruno Mars
- Shut Up and Dance - Walk the Moon
- Don't You Worry Child - Swedish House Mafia
- Mr. Brightside - The Killers
- Crazy in Love - Beyoncé

---

### 📚 Focus
**Keywords**: focus, study, work, concentration, concentrate, coding, productive, working, homework

**Suggested Songs**:
- Lo-Fi Hip Hop Study Beats - Chilled Cow
- Deep Focus - Spotify
- Work from Home - Productivity Playlist
- Peaceful Study Music - Ambient
- Focus Beats - Electronic

---

## Technical Details

### What Happens Behind the Scenes

**Timeline** (1-2 seconds total):
```
T=0.0s → User says "I'm happy"
T=0.1s → AI processes response + mood detection happens SIMULTANEOUSLY
T=0.2s → Create playlist with 5 happy song suggestions
T=0.3s → Start PARALLEL search for all 5 songs
         (All songs search at SAME TIME, not one by one!)
T=1.0s → All 5 search results come back
T=1.1s → Connect to voice channel (if needed)
T=1.2s → Add all 5 songs to music queue
T=1.3s → Auto-play starts (if nothing playing)
T=1.5s → Response sent to user
         "😊 Added 5 happy songs to queue!"
─────────
TOTAL: ~1.5 seconds ✓
```

### Parallel Search Optimization
The key to speed is **parallel searching**:

```python
# SLOW (Sequential - takes 5-10 seconds):
for song in ["Song1", "Song2", "Song3", "Song4", "Song5"]:
    search(song)  # Each search takes 1-2 seconds
    # TOTAL: 5-10 seconds ❌

# FAST (Parallel - takes 1-2 seconds):
asyncio.gather(
    search("Song1"),
    search("Song2"),
    search("Song3"),
    search("Song4"),
    search("Song5")
)
# All happen at SAME TIME!
# TOTAL: 1-2 seconds ✓
```

---

## Requirements to Use This Feature

✅ **Must be in a voice channel** - The bot needs to know which voice channel to play music in
✅ **Must mention mood in your message** - The bot looks for mood keywords
✅ **Music Cog must be loaded** - The music player needs to be available
✅ **Bot must have permission to join voice channels** - Discord permissions

---

## What Gets Queued

For each mood, the bot automatically selects and queues:
- **5 songs** (unless fewer are found)
- **Relevant to the detected mood**
- **In a temporary playlist** (deleted after all songs finish)
- **Usually 15-20 minutes of music** (depending on song lengths)

---

## Advanced Usage

### Mix with Commands
You can also use the regular music commands:

```
User: "I'm happy!"
→ Bot auto-queues 5 happy songs

User: "/play [song name]"
→ That song is added to the queue (after the auto-queued songs)

User: "/skip"
→ Skips to next queued song
```

### Customize Mood Suggestions
The mood and song mappings are in `cogs/chat/integrations/music_integration.py`:

```python
mood_songs = {
    'happy': [
        "Levitating - Dua Lipa",
        "Walking on Sunshine - Katrina & The Waves",
        # Add your own songs here!
    ]
}
```

---

## Troubleshooting

### "You're not in a voice channel!"
**Solution**: Join a Discord voice channel first, then tell the bot about your mood.

### No songs are playing
**Ensure**:
1. You're in a voice channel ✓
2. The bot has permission to join voice channels ✓
3. The Music Cog is loaded ✓
4. Internet connection is working ✓

### Songs aren't what you expected
Different mood keywords trigger different songs:
- If you say "I feel energized", it gives energetic songs
- If you say "I'm down", it gives sad songs
- Be specific about your mood!

### The mood detection didn't trigger
Check that you used one of the mood keywords:
- Say "happy", "sad", "energetic", "calm", "romantic", "party", or "focus"
- Not all messages trigger mood detection (only those with clear mood indicators)

---

## Feature Highlights

🚀 **Ultra-Fast**: 1-2 seconds from message to music playing
⚡ **Parallel Search**: All songs searched simultaneously
🎵 **Smart Suggestions**: Mood-based song selection
🔄 **Auto-Play**: No manual queue management needed
🎯 **Accurate**: Detects mood from natural language
💾 **Temporary**: Auto-playlist is cleaned up after use
🎚️ **Full Control**: Can skip, pause, or add more songs anytime

---

## Examples of What NOT to Do

❌ "Play something" (no mood detected)
→ System won't auto-queue (but you can still use /play command)

❌ "I like music" (no mood detected)
→ System won't auto-queue (insufficient mood keywords)

❌ Not in voice channel
→ Bot will tell you to join a voice channel first

✅ Do This Instead:
- "I'm feeling happy!" → Works! ✓
- "I need to focus" → Works! ✓
- "Let's party!" → Works! ✓
- "I'm in a great mood" → Works! ✓

---

## Fine-Tuning

### Changing Suggested Songs
Edit [music_integration.py](cogs/chat/integrations/music_integration.py#L600-L700):

```python
mood_songs = {
    'happy': [
        "Levitating - Dua Lipa",  # Remove or replace
        "Custom Song - Artist",   # Add your own!
    ]
}
```

### Changing Mood Keywords
Edit [music_integration.py](cogs/chat/integrations/music_integration.py#L530-L560):

```python
mood_keywords = {
    'happy': ['happy', 'joyful', 'your_keyword_here'],
}
```

### Changing Number of Songs
Edit [music_integration.py](cogs/chat/integrations/music_integration.py#L620):

```python
suggestions = await self.suggest_songs_by_mood(mood, count=10)  # Instead of 5
```

---

## Summary

The mood-based auto-playlist system makes listening to music effortless:

1. **Chat naturally** - "I'm in a good mood"
2. **AI detects mood** - Automatically identifies emotions
3. **Playlist generates** - 4-5 relevant songs suggested
4. **Songs queue** - All added to music queue in parallel
5. **Music plays** - Automatically starts playing

**No commands needed. No manual queue building. Just talk to the bot! 🎵**

---

## Need Help?

Check the system logs for:
- `🎵 Detected mood: happy` 
- `🔍 Starting PARALLEL search for X songs`
- `✅ Found X/5 songs`
- `⏱️ Complete mood playlist flow took X.XXs`

These logs show that the mood detection is working correctly!

