package org.psywerx.estudent;

public class MenuItem {
    private String name;
    private String description;
    private int icon;
    private int action;
    
	public MenuItem(String name, String description, int action, int icon) {
		this.name = name;
		this.description = description;
		this.action = action;
		this.icon = icon;
	}
	public MenuItem(String name, String description, int action) {
		this.name = name;
		this.description = description;
		this.action = action;
		this.icon = -1;
	}
	public String getName() { return name; }		
	public String getDescription() { return description; }
	public int getAction() { return action; }
	public boolean haveIcon() { return icon != -1; }
	public int getIcon() { return icon; }
}