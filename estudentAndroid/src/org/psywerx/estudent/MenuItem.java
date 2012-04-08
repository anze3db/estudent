package org.psywerx.estudent;

public class MenuItem {
	
	public static final int LOGOUT_ICON = 0;
	public static final int NOTEPAD_ICON = 1;
	
	
    private String itemName;
    private String itemDescription;
    private int action;
    private int icon;

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
    public void setIcon(int icon) {
		this.icon = icon;
	}
    public int getIcon() {
		return icon;
	}
}