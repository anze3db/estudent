package org.psywerx.estudent;

import org.psywerx.estudent.json.User;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.text.InputType;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

public class LoginActivity extends Activity implements ResponseListener{

	private EditText mEditUsername;
	private EditText mEditPassword;
	private Button mBtnConfirm;
	private ResponseListener mListener;

	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.login_layout);
		init();
	}

	private void init() {

		mListener = this;
		mEditUsername = (EditText) findViewById(R.id.eUsername);
		mEditPassword = (EditText) findViewById(R.id.ePassword);
		mBtnConfirm = (Button) findViewById(R.id.btnConfirm);
		mBtnConfirm.requestFocus();
		setListeners();
	}

	private void setListeners(){
		mEditUsername.setOnFocusChangeListener(new View.OnFocusChangeListener() {
			public void onFocusChange(View v, boolean focus) {
				changedFocus((EditText) v,focus,getString(R.string.edit_text_username),false);
			}
		});
		mEditPassword.setOnFocusChangeListener(new View.OnFocusChangeListener() {
			public void onFocusChange(View v, boolean focus) {
				changedFocus((EditText) v,focus,getString(R.string.edit_text_password),true);
			}
		});

		mBtnConfirm.setOnClickListener(new View.OnClickListener() {
			public void onClick(View v) {
				String username = mEditUsername.getText().toString();
				String password = mEditPassword.getText().toString();
				if (username.equals(getString(R.string.edit_text_username)) || 
						mEditUsername.length() == 0 ) {
					mEditUsername.setError(getText(R.string.error_required));
					return;
				}
				if (password.equals(getString(R.string.edit_text_password)) ||
						mEditPassword.length() == 0 ) {
					mEditPassword.setError(getText(R.string.error_required));
					return;
				}
				Api.loginRequest(mListener, username, password);
			}
		});
	}

	protected void changedFocus(EditText v, boolean hasFocus, String message, boolean isPassword) {
		if (hasFocus){
			if (v.getText().toString().equals(message)){
				v.setText("");
				if (isPassword){
					v.setInputType(InputType.TYPE_TEXT_VARIATION_PASSWORD | 
							InputType.TYPE_CLASS_TEXT);
				}
				v.setTextColor(getResources().getColor(R.color.black));
			}
		}else{
			if (v.length()==0){
				v.setText(message);
				if (isPassword){
					v.setInputType(InputType.TYPE_TEXT_VARIATION_NORMAL | 
							InputType.TYPE_CLASS_TEXT);
				}
				v.setTextColor(getResources().getColor(R.color.gray));
			}
		}
	}

	@Override
	protected void onResume() {
		super.onResume();
		mEditPassword.setText("");
		mEditUsername.setText("");
		changedFocus(mEditPassword, false, getString(R.string.edit_text_password), true);
		changedFocus(mEditUsername, false, getString(R.string.edit_text_username), false);
	}
	
	public void onServerResponse(Object o) {
		if (o != null){
			User user = (User) o;
			if (user.getLogin() ||  true){
				Intent intent = new Intent(this, MenuActivity.class);
			    Bundle bundle = new Bundle();
			    bundle.putString("firstname", user.getName());
			    bundle.putString("lastname", user.getSurname());
			    bundle.putString("username", mEditUsername.getText().toString());
			    bundle.putString("password", mEditPassword.getText().toString());
			    intent.putExtras(bundle);
				startActivity(intent);
			}
		}
	}
}
