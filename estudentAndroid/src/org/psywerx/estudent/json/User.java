package org.psywerx.estudent.json;

public class User {
	protected String firstname;
	protected String lastname;
	protected boolean login;
	protected boolean locked;
	
	public String getFirstname() {
		return firstname;
	}
	public String getLastname() {
		return lastname;
	}
	public boolean getLogin() {
		return login;
	}
	public void setFirstname(String firstname) {
		this.firstname = firstname;
	}
	public void setLastname(String lastname) {
		this.lastname = lastname;
	}
	public void setLogin(boolean login) {
		this.login = login;
	}
	public void setLocked(boolean locked) {
		this.locked = locked;
	}
	public boolean getLocked() {
		return locked;
	}
}
