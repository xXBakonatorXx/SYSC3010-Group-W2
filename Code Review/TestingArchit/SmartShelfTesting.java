/**
 * Client code for SmartShelf
 * Group: W10
 */
package smartshelftesting;

public class SmartShelfTesting {

    private int numItems; // the number of items on the shelf on the shelf 
    private int numItemAdd; // the number of items added to the shelf 
    private double price; // the current price of the item on shelf 

    // The constructor for the smart shelf testing
    public SmartShelfTesting(int numItems, int numItemAdd, double price) {

        this.numItems = numItems;
        this.numItemAdd = numItemAdd;
        this.price = price;

    }

    public int getNumItems() { // gets the value of the numItems from constructor
        return this.numItems;
    }

    public int getNumItemAdd() { // gets the value of the numItemAdd from constructor
        return this.numItemAdd;
    }

    public double getPrice() { // gets the value of the price from constructor
        return this.price;
    }

    public boolean ItemOnShelf(double dist) { //checks if there are items on the shelf
        if (dist > 0.0) { //if the servo distance is more than 0 then there are items on shelf
            return true;
        } else {
            return false;
        }
    }

    public boolean ItemRemove(int newItems) { //checks if an item has been removed from the shelf
        if (numItems < newItems) { //if the the numItems is less than the calculated new number of items the items were removed
            return true;
        } else {
            return false;
        }
    }

    public boolean ItemAdd(int numItems) { //checks if an itema has been add to the shelf 
        if (numItemAdd > numItems) { //if the the numItemsAdd is greater than the calculated new number of items the items were added 
            return true;
        } else {
            return false;
        }
    }

    public boolean ItemPriceChange(double newPrice) { //checks if the price was changed
        if (price == newPrice) { //if the old price is the same as the new price then no price change
            return false;
        } else {
            return true;
        }

    }

}
