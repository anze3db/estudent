package org.psywerx.estudent;

public class MenuItem {
	   
    private String itemName;
    private String itemDescription;
    private int action;

    public MenuItem() {
	}
    public MenuItem(String itemName, String itemDescription, int action) {
    	this.itemName = itemName;
    	this.itemDescription = itemDescription;
    	this.action = action;
	}
    
    public String getItemName() {
        return itemName;
    }
    public void setItemName(String orderName) {
        this.itemName = orderName;
    }
    public String getItemDescription() {
        return itemDescription;
    }
    public void setItemDescription(String orderStatus) {
        this.itemDescription = orderStatus;
    }
    public int getAction() {
		return action;
	}
    public void setAction(int action) {
		this.action = action;
	}
}