/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package S.S;

import org.junit.Test;
import static org.junit.Assert.*;
import smartshelftesting.SmartShelfTesting;

/**
 * Test code for SmartShelf to test possible cases for client code Group: W10
 */
public class Testing {

    public Testing() {

    }

    @Test
    public void testConstrustor() { // Tests the that constructor inputs are valid
        SmartShelfTesting t = new SmartShelfTesting(5, 6, 3.99);
        assertEquals(5, t.getNumItems()); // checks the input numItems is valid input
        assertEquals(6, t.getNumItemAdd()); //checks the input numItemAdd is valid input
        assertEquals(3.99, t.getPrice(), 0.001); //checks the input price is a valid input
    }

    @Test
    public void testItemOnShelf() { //tests for ItemOnShelf

        SmartShelfTesting d = new SmartShelfTesting(0, 0, 0);
        assertEquals(false, d.ItemOnShelf(0)); //test if no items on shelf case works
        assertEquals(true, d.ItemOnShelf(3.5)); //test if items on shelf case works
    }

    @Test
    public void testItemRemove() { //tests for item removal

        SmartShelfTesting j = new SmartShelfTesting(3, 0, 0);
        assertEquals(true, j.ItemRemove(5)); //tests if item remove case works
        assertEquals(false, j.ItemRemove(2)); //tests if no item remove case works
    }

    @Test
    public void testItemAdd() { //tests if an item has been added

        SmartShelfTesting c = new SmartShelfTesting(3, 4, 0);
        assertEquals(true, c.ItemAdd(2)); //tests if item added case works
        assertEquals(false, c.ItemAdd(5)); //tests if item not added case works

    }

    @Test
    public void testItemPriceChange() { // test if the price has been changed

        SmartShelfTesting a = new SmartShelfTesting(5, 0, 2.99);
        assertEquals(false, a.ItemPriceChange(2.99)); // tests if the price is the same 
        assertEquals(true, a.ItemPriceChange(3.50)); // tests if the price is not the same
    }

}
