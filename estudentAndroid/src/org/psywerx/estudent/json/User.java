package org.psywerx.estudent.json;

public class User {
	protected String firstname;
	protected String lastname;
	protected boolean login;
	
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
}
