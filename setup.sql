-- Create the Customer table
CREATE TABLE Customer (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,  -- auto-incrementing integer for unique IDs
    name VARCHAR(255) NOT NULL,                  -- name as a string with max length of 255
    email VARCHAR(255) NOT NULL UNIQUE,          -- email as a unique string
    password VARCHAR(255) NOT NULL,              -- password as a string
    phone VARCHAR(20),                           -- phone number, assuming no more than 20 chars
    address TEXT                                 -- address as a long text field
);

-- Create the Package table
CREATE TABLE Package (
    package_id INT AUTO_INCREMENT PRIMARY KEY,   -- auto-incrementing integer for unique package IDs
    customer_id INT,                             -- customer_id as a foreign key
    source VARCHAR(255) NOT NULL,                -- source location as a string
    destination VARCHAR(255) NOT NULL,           -- destination location as a string
    current_location VARCHAR(255) NOT NULL,      -- current location of the package
    status VARCHAR(50),                          -- package status (e.g., "In Transit")
    weight DECIMAL(10, 2),                       -- weight of the package (up to 99999999.99)
    pick_up_date DATE,                           -- pick-up date (formatted as YYYY-MM-DD)
    delivery_option VARCHAR(100),                -- delivery option (e.g., "Standard", "Express")
    expected_delivery_date DATE,                 -- expected delivery date
    cost DECIMAL(10, 2),                         -- cost of the package
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id)  -- foreign key constraint
);

