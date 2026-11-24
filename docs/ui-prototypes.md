# UI Prototypes

This document captures the initial low-fidelity interface concepts for the AI-Enabled Bookstore. It is intended as a shared implementation reference; labels, sample books, prices, and ratings are illustrative rather than final product data.

## 5.1 Homepage and Catalog UI

The homepage serves as the central hub for user interaction, providing unified access to book search, catalog navigation, personalized AI recommendations, and account options.

### Homepage wireframe

```text
+--------------------------------------------------------------------------------+
| [Logo] Libjaras AI-Enabled Bookstore                         [Search Bar...]    |
| [Search]                                                                       |
| [Home] [Catalog] [Categories v] [My Orders] [AI Chat Assistant]                |
| (Profile/Login)                                                                |
+--------------------------------------------------------------------------------+
| BANNER: AI-Powered Visual Search & Personalized Recommendations                |
|                                                                                |
| [ Upload Cover Image for Visual Search ]                                       |
+--------------------------------------------------------------------------------+
| AI RECOMMENDED FOR YOU                                                         |
|                                                                                |
| +----------------------+  +----------------------+  +----------------------+   |
| |    [ Cover Image ]   |  |    [ Cover Image ]   |  |    [ Cover Image ]   |   |
| | Title: Book A        |  | Title: Book B        |  | Title: Book C        |   |
| | Author: Author X     |  | Author: Author Y     |  | Author: Author Z     |   |
| | Rating: 4.8/5        |  | Rating: 4.5/5        |  | Rating: 4.9/5        |   |
| | Price: $19.99        |  | Price: $14.99        |  | Price: $24.99        |   |
| | [ View Details ]     |  | [ View Details ]     |  | [ View Details ]     |   |
| +----------------------+  +----------------------+  +----------------------+   |
+--------------------------------------------------------------------------------+
| CATALOG BROWSE                                                                 |
| Filter by: [Genre v] [Author v] [Price Range v]  [Sort: Popular v]             |
|                                                                                |
| +----------------------+  +----------------------+  +----------------------+   |
| |    [ Cover Image ]   |  |    [ Cover Image ]   |  |    [ Cover Image ]   |   |
| | Title: Book D        |  | Title: Book E        |  | Title: Book F        |   |
| | [ Buy Now ]          |  | [ Buy Now ]          |  | [ Buy Now ]          |   |
| +----------------------+  +----------------------+  +----------------------+   |
+--------------------------------------------------------------------------------+
```

### Functional intent

- Provide persistent access to search, catalog categories, orders, the AI assistant, and authentication/profile controls.
- Promote AI-powered visual search by allowing a user to upload a book-cover image.
- Show personalized recommendations with a cover, title, author, rating, price, and link to the book details.
- Let users browse the broader catalog and narrow results by genre, author, and price range.
- Let users sort catalog results, with popularity shown as the initial example.
- Provide a direct purchase action from each catalog card.

## 5.2 AI Chat Assistant Interaction

The AI Chat Assistant provides real-time natural-language query resolution, context-aware recommendations, and personalized catalog navigation assistance.

### Assistant wireframe

```text
+--------------------------------------------------------------------------------+
| AI Chat Assistant                                                          [X] |
+--------------------------------------------------------------------------------+
| AI: Hello Jamis! How can I assist you with your book search today?             |
|                                                                                |
| User: Can you recommend a sci-fi novel similar to Dune with great               |
|       world-building?                                                          |
|                                                                                |
| AI: Based on your preference for detailed world-building, here are 2 top picks:|
|                                                                                |
|     1. "Foundation" by Isaac Asimov (Rating: 4.7/5 - $12.99)                   |
|                                                                                |
|     2. "Hyperion" by Dan Simmons (Rating: 4.6/5 - $15.99)                     |
|                                                                                |
|     Would you like me to show full descriptions or add one to your cart?       |
|                                                                                |
| User: Show me the description for Hyperion.                                    |
|                                                                                |
| AI: "Hyperion" follows seven pilgrims traveling to the world of Hyperion to   |
|     seek answers from the Shrike. It explores complex themes across multiple   |
|     storylines.                                                                |
|                                                                                |
|     [ View Book Page ]  [ Add to Cart ]                                         |
+--------------------------------------------------------------------------------+
| [ Type your message or prompt here...                              ] [ Send ]   |
+--------------------------------------------------------------------------------+
```

### Functional intent

- Greet authenticated users by name and invite a natural-language book query.
- Use conversational context and stated preferences to recommend relevant books.
- Include useful decision data such as author, rating, and price in recommendations.
- Support follow-up questions without requiring the user to repeat prior context.
- Offer actionable next steps from the conversation, including opening the book page and adding a book to the cart.
- Keep a message input and send action available at the bottom of the assistant.

## Implementation reference

The prototypes imply the following reusable interface areas:

| Area | Main elements |
| --- | --- |
| Global navigation | Logo, search, primary links, category menu, profile/login |
| Visual search | Promotional banner, cover-image upload control |
| Recommendations | Personalized book-card collection |
| Catalog | Filter controls, sort control, book-card grid, purchase actions |
| AI assistant | Conversation history, contextual recommendations, book actions, message composer |

When implementation begins, accessibility and responsive behavior should be treated as requirements: interactive controls need visible labels and keyboard focus states, uploaded images need clear validation and status feedback, and multi-column book grids should collapse cleanly on smaller screens.
