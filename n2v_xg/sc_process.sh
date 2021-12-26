echo "Dimension,Epochs,Length_of_Walk,Num_Walks,Context_Size,Return_Hyperparam,Accuracy,Balanced_Accuracy,F1_Score,Matthews_Corrcoef,Roc_Auc,Precision,Recall" > log/last1.csv
echo "Dimension,Epochs,Length_of_Walk,Num_Walks,Context_Size,Return_Hyperparam,Accuracy,Balanced_Accuracy,F1_Score,Matthews_Corrcoef,Roc_Auc,Precision,Recall" > log/last2.csv
echo "Dimension,Epochs,Length_of_Walk,Num_Walks,Context_Size,Return_Hyperparam,Accuracy,Balanced_Accuracy,F1_Score,Matthews_Corrcoef,Roc_Auc,Precision,Recall" > log/last3.csv
echo "Dimension,Epochs,Length_of_Walk,Num_Walks,Context_Size,Return_Hyperparam,Accuracy,Balanced_Accuracy,F1_Score,Matthews_Corrcoef,Roc_Auc,Precision,Recall" > log/last4.csv

for dim in 32 64
do
    for epochs in 5 10
    do
        for length in 80 120
        do
            for walk in 10 20
            do
                for cont in 5 10 20
                do
                    for retpar in 0.5 1 1.5
                    do
                        FILE="${PWD}/emb/sc_ppi_emb_d${dim}_e${epochs}_l${length}_w${walk}_k${cont}_p${retpar}.emb"
                        if [ -f $FILE ]; then
                            echo "$FILE exists"
                            python3 subcellular_localization.py $FILE &
                            python3 gene_expression.py $FILE &
                            wait
                            for option in 1 2 3 4
                            do
                                python3 embedding.py $FILE $option
                                log_file="log/last${option}.csv"
                                echo -n "${dim},${epochs},${length},${walk},${cont},${retpar}," >> $log_file
                                if [[ $option -eq 1 ]]
                                then
                                    emb_filename="csv_imp/sc_ppi_emb_d${dim}_e${epochs}_l${length}_w${walk}_k${cont}_p${retpar}.emb.csv"
                                    es_filename="csv_imp/sc_ppi_emb_d${dim}_e${epochs}_l${length}_w${walk}_k${cont}_p${retpar}.emb_out.csv"
                                    python3 boost.py $emb_filename $es_filename $option >> $log_file                                
                                elif [[ $option -eq 2 ]]
                                then
                                    emb_filename="csv_imp_sl/sc_ppi_emb_d${dim}_e${epochs}_l${length}_w${walk}_k${cont}_p${retpar}.emb.csv"
                                    es_filename="csv_imp_sl/sc_ppi_emb_d${dim}_e${epochs}_l${length}_w${walk}_k${cont}_p${retpar}.emb_out.csv"
                                    python3 boost.py $emb_filename $es_filename $option >> $log_file
                                elif [[ $option -eq 3 ]]
                                then
                                    emb_filename="csv_imp_ge/sc_ppi_emb_d${dim}_e${epochs}_l${length}_w${walk}_k${cont}_p${retpar}.emb.csv"
                                    es_filename="csv_imp_ge/sc_ppi_emb_d${dim}_e${epochs}_l${length}_w${walk}_k${cont}_p${retpar}.emb_out.csv"
                                    python3 boost.py $emb_filename $es_filename $option >> $log_file
                                else
                                    emb_filename="csv_imp_sl_ge/sc_ppi_emb_d${dim}_e${epochs}_l${length}_w${walk}_k${cont}_p${retpar}.emb.csv"
                                    es_filename="csv_imp_sl_ge/sc_ppi_emb_d${dim}_e${epochs}_l${length}_w${walk}_k${cont}_p${retpar}.emb_out.csv"
                                    python3 boost.py $emb_filename $es_filename $option >> $log_file
                               fi
                           done
                        fi
                    done
                done
            done
        done
    done
done
