# Personal Expense Tracker

A comprehensive web-based expense tracking application built with Python and Streamlit, featuring group expense management and detailed analytics.

## 🌟 Features

### Core Functionality
- **Multi-user Group Management**: Create or join expense groups using shared group IDs
- **Category Management**: Add and manage custom expense categories
- **Payment Options**: Configure multiple payment methods
- **Transaction Recording**: Track payments, transfers, and income
- **Real-time Analytics**: Comprehensive expense analysis and visualization

### Key Sections
1. **Category Management** - Add and manage expense categories
2. **Payment Options** - Configure multiple payment methods
3. **Payment Processing** - Record expenses with mobile payment app integration (Paytm, Google Pay, PhonePe)
4. **Transfer Tracking** - Monitor money transfers between accounts
5. **Income Recording** - Track all income sources
6. **Transaction History** - View monthly transactions and payment balances
7. **Expenditure Analysis** - Detailed analytics including:
   - Per-user total expenses
   - Category-wise expense breakdown
   - Interactive pie charts
   - Monthly summaries
8. **User Authentication** - Secure login and registration system with group management:
   - **New User Registration**: Create account and get new group ID
   - **Join Existing Group**: Register with existing group ID to join family/friends
   - **Group Sharing**: Share group ID to invite others to your expense group
9. **Login Page** - Secure user authentication
10. **Register Page** - New user registration with group creation/joining options

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **Database**: MongoDB
- **Deployment**: Streamlit Community Cloud
- **Version Control**: GitHub

## 📋 Prerequisites

- Python 3.7+
- MongoDB Atlas account or local MongoDB installation
- Git
- **For Mobile Payment Features**: Mobile device with payment apps redirection (Paytm/GPay/PhonePe)

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/niket1007/personal_resume_website.git
cd personal_resume_website
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Database Connection
Create a `.streamlit` folder in your project root and add a `secrets.toml` file:

```toml
[mongodb]
connection_string = "your_mongodb_connection_string_here"
```

**Note**: Replace `your_mongodb_connection_string_here` with your actual MongoDB connection string.

### 4. Run the Application
```bash
streamlit run app.py
```

## 👥 Group Management

### Creating a New Group
- Register without providing a group ID
- System automatically creates a new expense group
- You receive a unique group ID to share with others

### Joining an Existing Group
- During registration, provide an existing group ID
- System adds you to the specified group
- Start tracking shared expenses immediately

### Group Benefits
- **Shared Expenses**: Track group spending like family expenses, roommate costs, or travel expenses
- **Individual Tracking**: See each member's contribution and spending patterns
- **Collaborative Budgeting**: Work together on expense categories and budgets
- **Real-time Updates**: All group members see transactions and balances instantly

## 📊 Database Structure

### Main Database Collections:
- **login**: Stores user authentication data
  - `username`: User's login name
  - `password`: User's password (hashed)

- **group_user**: Manages group memberships
  - `group_id`: Unique identifier for expense groups
  - `username`: Associated username

### Group-Specific Databases:
Each group gets its own database (named after the group ID) containing:
- **categories**: Expense categories
- **payment_options**: Available payment methods
- **transaction_records**: All financial transactions

## 🔐 User Authentication Flow

### Registration Process
1. **New Group Creation**: 
   - Register without providing a group ID
   - System creates a new group and assigns a unique group ID
   - Share this group ID with family/friends to join your expense group

2. **Join Existing Group**:
   - Register by providing an existing group ID
   - System adds you to the specified expense group
   - You can now track expenses together with other group members

### Login Process
3. **User Login**: Existing users login with their credentials
4. **Group Association**: System automatically loads the user's associated expense group

## 📱 Mobile Payment Integration

The application includes seamless integration with popular payment apps for mobile users:

### Supported Payment Apps:
- **Paytm**
- **Google Pay (GPay)**
- **PhonePe**

### How It Works:
1. **Record Expense**: Enter the amount in payment section and select payment method
2. **Mobile Redirect**: When accessed on mobile devices, clicking submit displays a dialog box with available payment apps. Select your preferred app to redirect and complete the payment
3. **Complete Payment**: The respective payment app opens automatically to complete the transaction

### Requirements:
- **Mobile Device**: Payment app redirection works only on mobile devices
- **Installed Apps**: The selected payment app (Paytm/GPay/PhonePe) must be installed on your device
- **App Permissions**: Allow the browser to open external apps

### Note:
This feature provides convenient payment processing for mobile users. On desktop, the expense is recorded for tracking purposes without payment app redirection.

## 📈 Analytics Dashboard

The expenditure analysis section provides:
- **User-wise Expenses**: Track spending per user in the group
- **User-wis Category Analysis**: Breakdown of expenses by category for each user
- **Visual Reports**: Interactive pie charts and tables
- **Monthly Summaries**: Time-based expense tracking
- **Balance Tracking**: Real-time balance across payment options


## 📁 Project Structure

```
personal_resume_website/
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── .streamlit/
│   └── secrets.toml      # Configuration file (not in repo)
├── pages/                # Streamlit pages
├── utils/                # Helper functions
└── README.md
```

### Security Notes
- Never commit your `secrets.toml` file to the repository
- Use environment variables for production deployments
- Ensure your MongoDB connection string includes proper authentication

## 🐛 Troubleshooting

### Common Issues:
1. **Database Connection Error**: Verify your MongoDB connection string in `secrets.toml`
2. **Module Not Found**: Run `pip install -r requirements.txt`
3. **Streamlit Not Starting**: Ensure you're in the correct directory and have Streamlit installed
4. **Payment App Not Opening**: 
   - Ensure you're using a mobile device
   - Check that the selected payment app is installed
   - Allow browser permissions to open external apps

---