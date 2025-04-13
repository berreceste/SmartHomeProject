package com.example.smarthome.auth

import android.util.Log
import com.google.firebase.auth.FirebaseAuth

object AuthManager {
    private val auth = FirebaseAuth.getInstance()

    fun registerUser(email: String, password: String) {
        auth.createUserWithEmailAndPassword(email, password)
            .addOnCompleteListener { task ->
                if (task.isSuccessful) {
                    Log.d("AUTH", "Registered: ${auth.currentUser?.uid}")
                } else {
                    Log.e("AUTH", "Register failed: ${task.exception?.message}")
                }
            }
    }

    fun loginUser(email: String, password: String) {
        auth.signInWithEmailAndPassword(email, password)
            .addOnSuccessListener {
                Log.d("AUTH", "Login successful")
            }
            .addOnFailureListener {
                Log.e("AUTH", "Login failed: ${it.message}")
            }
    }
} 