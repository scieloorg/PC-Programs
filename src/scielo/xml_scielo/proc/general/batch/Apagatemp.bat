@echo off
md temp
cd temp
for %%i in (*.*) do del %%i
cd..
md PubMed
cd PubMed
for %%i in (*.*) do del %%i
cd..
