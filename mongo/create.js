db.dropDatabase()
db.createCollection('used_urls')
db.urls.createIndex({ short_url: 1 }, { unique: true });

// Create 'urls' collection with original_url and short_url as keys
db.createCollection('urls')

db.urls.createIndex({ original_url: 1 }, { unique: true });
db.urls.createIndex({ short_url: 1 }, { unique: true });

// Create 'users' collection
db.createCollection('users');

db.users.createIndex({ email: 1 }, { unique: true });

// Insert initial data into 'users' collection
db.users.insertOne({
  name: "Ravid H",
  email: "ravidh@example.com",
  creationDate: new Date()
});
